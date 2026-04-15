from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.Column(db.JSON, default={})
    
    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy=True)
    evaluations = db.relationship('Evaluation', backref='user', lazy=True)
    aptitude_results = db.relationship('AptitudeResult', backref='user', lazy=True)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255))
    parsed_content = db.Column(db.JSON)  # Stores extracted skills, experience etc
    raw_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    company = db.Column(db.String(255))
    raw_text = db.Column(db.Text, nullable=False)
    parsed_requirements = db.Column(db.JSON)  # Stores mandatory_skills, preferred_skills etc
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    jd_id = db.Column(db.Integer, db.ForeignKey('job_description.id'), nullable=True) # Optional, can be general eval
    
    overall_score = db.Column(db.Integer)
    jd_match_score = db.Column(db.Integer)
    
    missing_skills = db.Column(db.JSON) # Critical, Upskilling, Trending
    recommendations = db.Column(db.JSON) # Courses, Projects
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class AptitudeResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    top_domain = db.Column(db.String(100))
    score = db.Column(db.Float)
    confidence = db.Column(db.String(50))
    
    strengths = db.Column(db.JSON)
    improvement_areas = db.Column(db.JSON)
    secondary_domains = db.Column(db.JSON)
    
    full_analysis = db.Column(db.JSON) # Detailed scores for all domains
    responses = db.Column(db.JSON) # Raw user responses
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(100)) # Aptitude, Domain Specific
    topic = db.Column(db.String(100))
    difficulty = db.Column(db.Integer) # 1: Easy, 2: Medium, 3: Hard
    question_data = db.Column(db.JSON) # {question, options, answer, explanation}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_id = db.Column(db.String(100)) # To group test sessions
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    topic = db.Column(db.String(100))
    difficulty_level = db.Column(db.Integer)
    user_answer = db.Column(db.String(255))
    correct_answer = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean)
    time_taken = db.Column(db.Integer)  # seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TopicPerformance(db.Model):
    __tablename__ = 'topic_performance'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic = db.Column(db.String(100))
    total_questions = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    accuracy_percentage = db.Column(db.Float, default=0.0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserReward(db.Model):
    __tablename__ = 'user_rewards'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_xp = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    max_streak = db.Column(db.Integer, default=0)
    badges_earned = db.Column(db.JSON, default=list) # e.g. ["Speed Master"]
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

