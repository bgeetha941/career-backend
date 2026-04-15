from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime, timedelta
import os

# Import Models
from models import db, User, Resume, JobDescription
from sqlalchemy import or_

# Import Blueprints from restored files
from stream import stream_bp
from adaptive_mocktest import adaptive_test_bp
# from career_analysis import career_bp  # Removed: no active routes
from services.resume_parser import ResumeParser
from services.jd_parser import JobDescriptionParser
from services.career_analyzer import CareerAnalyzer
from services.ai_analyzer import AICareerAnalyzer

app = Flask(__name__)
# Enable CORS for all routes with explicit support for Authorization header
CORS(app, resources={r"/api/*": {"origins": "*"}}, expose_headers=["Authorization"], allow_headers=["*"])

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leanleap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
db.init_app(app)

# Initialize Services used directly in main
resume_parser = ResumeParser()
jd_parser = JobDescriptionParser()
career_analyzer = CareerAnalyzer()
# You should add your GEMINI_API_KEY to your environment or replace here
GEMINI_API_KEY = "AIzaSyAvUPwj4N9gxZE9lkEMmIeaXHIu762MSmo" 
ai_career_analyzer = AICareerAnalyzer(api_key=GEMINI_API_KEY)

# Register Blueprints
app.register_blueprint(stream_bp, url_prefix='/api/streams')
app.register_blueprint(adaptive_test_bp, url_prefix='/api/adaptive-test')
# from career_analysis import career_bp  # Removed: no active routes
# Create tables
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@leanleap.com').first():
        admin = User(
            email='admin@leanleap.com',
            name='Admin User',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()

# ==================== AUTHENTICATION ENDPOINTS (For Flutter) ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'error': 'Missing required fields'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User already exists'}), 409
    
    new_user = User(
        email=data['email'],
        name=data['name'],
        password_hash=generate_password_hash(data['password']),
        role=data.get('role', 'student')
    )
    db.session.add(new_user)
    db.session.commit()
    
    access_token = create_access_token(identity=new_user.email)
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': {'email': new_user.email, 'name': new_user.name, 'role': new_user.role}
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.email)
    return jsonify({
        'success': True,
        'access_token': access_token,
        'user': {'email': user.email, 'name': user.name, 'role': user.role}
    }), 200

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'email': user.email, 'name': user.name, 'role': user.role, 'profile': user.profile
    }), 200

@app.route('/api/auth/profile/update', methods=['POST'])
@jwt_required()
def update_profile():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    data = request.get_json()
    profile = user.profile or {}
    profile['is_public'] = data.get('is_public', profile.get('is_public', False))
    profile['phone'] = data.get('phone', profile.get('phone', ''))
    profile['name'] = data.get('name', profile.get('name', user.name))
    profile['email'] = data.get('email', profile.get('email', user.email))
    
    # Needs to reassign to trigger SQLAlchemy JSON modification tracking if not using MutableDict
    user.profile = profile
    db.session.commit()
    
    return jsonify({'success': True, 'profile': user.profile}), 200

# ==================== RESUME & JD PARSING ENDPOINTS ====================

@app.route('/api/resume/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    print(f"[{datetime.now()}] POST /api/resume/upload - Request received")
    print(f"Request headers: {request.headers}")
    
    email = get_jwt_identity()
    print(f"User identity from JWT: {email}")
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'success': False, 'error': 'User not found', 'data': {}}), 404
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part', 'data': {}}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file', 'data': {}}), 400
        
    # Check for existing analysis (Caching)
    existing_resume = Resume.query.filter_by(user_id=user.id, filename=file.filename).first()
    if existing_resume and existing_resume.parsed_content:
        print("[CACHE] Found existing analysis for this resume. Returning immediately.")
        return jsonify({
            'success': True,
            'message': 'Retrieved from history',
            'resume_id': existing_resume.id,
            'data': existing_resume.parsed_content,
            'is_new': False
        }), 200

    parsed_data = resume_parser.parse_resume(file)
    if 'error' in parsed_data:
        return jsonify({'success': False, 'error': parsed_data['error'], 'data': {}}), 400
        
    resume = Resume(
        user_id=user.id,
        filename=file.filename,
        parsed_content=parsed_data,
        raw_text=parsed_data.get('raw_text', '')   
    )
    db.session.add(resume)
    db.session.commit()
    
    # Perform AI Analysis
    jd_text = request.form.get('jd_text', '')
    if jd_text:
        if ai_career_analyzer.model and GEMINI_API_KEY:
            # Use Gemini for comprehensive analysis
            analysis_data = ai_career_analyzer.analyze_with_ai(parsed_data.get('raw_text', ''), jd_text)
            
            # Save the AI analysis result back into our database for future fast access
            resume.parsed_content = analysis_data
            db.session.commit()
            
            if not analysis_data.get('success', False):
                print(f"AI Analysis failed ({analysis_data.get('error')}). Falling back to Rule-Based.")
                parsed_jd = jd_parser.parse_jd(jd_text)
                analysis_data = career_analyzer.evaluate_resume_against_jd(parsed_data, parsed_jd)
                analysis_data['success'] = True # Rule-based is success
                analysis_data['fit_level'] += " (Rule-based)" # Indicate fallback
        else:
            # Normal rule-based if NO key is set
            parsed_jd = jd_parser.parse_jd(jd_text)
            analysis_data = career_analyzer.evaluate_resume_against_jd(parsed_data, parsed_jd)
            analysis_data['success'] = True
    else:
        # Fallback to general career analysis
        analysis_data = career_analyzer.analyze_resume(parsed_data)

    return jsonify({
        'success': True,
        'message': 'Uploaded and Analyzed', 
        'resume_id': resume.id, 
        'data': analysis_data
    }), 201

@app.route('/api/resume/analyze-ai', methods=['POST'])
@jwt_required()
def analyze_resume_ai():
    """Perform AI-powered analysis using Gemini"""
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file part',
            'data': {}
        }), 400
    file = request.files['file']
    jd_text = request.form.get('jd_text', '')
    
    if not jd_text:
        return jsonify({
            'success': False,
            'error': 'Job description text is required for AI analysis',
            'data': {}
        }), 400

    # 1. Parse Resume for text
    parsed_resume = resume_parser.parse_resume(file)
    if 'error' in parsed_resume:
        return jsonify({
            'success': False,
            'error': parsed_resume['error'],
            'data': {}
        }), 400
    
    # 2. Save to database
    resume = Resume(
        user_id=user.id,
        filename=file.filename,
        parsed_content=parsed_resume,
        raw_text=parsed_resume.get('raw_text', '')
    )
    db.session.add(resume)
    db.session.commit()

    # 3. Perform AI Analysis
    ai_results = ai_career_analyzer.analyze_with_ai(
        resume_text=parsed_resume.get('raw_text', ''),
        jd_text=jd_text
    )

    # CRITICAL FALLBACK: If AI fails, use Rule-based to ensure the user gets a result
    if not ai_results.get('success', False):
        print(f"AI Analysis (/analyze-ai) failed: {ai_results.get('error')}. Switching to Rule-Based.")
        parsed_jd = jd_parser.parse_jd(jd_text)
        fallback_data = career_analyzer.evaluate_resume_against_jd(parsed_resume, parsed_jd)
        fallback_data['success'] = True
        
        return jsonify({
            'success': True,
            'message': 'AI Analysis failed, but Rule-based analysis succeeded',
            'resume_id': resume.id,
            'data': fallback_data
        }), 200

    return jsonify({
        'success': True,
        'resume_id': resume.id,
        'data': ai_results
    }), 200

@app.route('/api/jd/parse', methods=['POST'])
@jwt_required()
def parse_jd():
    data = request.get_json()
    if not data or not data.get('jd_text'):
        return jsonify({'error': 'Missing jd_text'}), 400
        
    jd_text = data['jd_text']
    parsed_jd = jd_parser.parse_jd(jd_text)
    jd = JobDescription(title=parsed_jd.get('job_title', 'Unknown'), raw_text=jd_text, parsed_requirements=parsed_jd)
    db.session.add(jd)
    db.session.commit()
    
    return jsonify({'message': 'Parsed successfully', 'jd_id': jd.id, 'parsed_jd': parsed_jd}), 201




@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    print("Starting Flask API with SQLite Database on port 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)
