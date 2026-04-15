from google import genai
from google.genai import types
import json
import re

class AICareerAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            self.ready = True
        else:
            self.client = None
            self.ready = False
        # Keep a model attribute for compatibility checks in main.py
        self.model = self.ready

    def analyze_with_ai(self, resume_text, jd_text):
        if not self.ready:
            return {"success": False, "error": "AI API Key not configured"}

        prompt = f"""
        You are a highly advanced HR AI and Career Analysis System. 
        Analyze the provided Resume and Job Description DYNAMICALLY.

        RESUME TEXT:
        {resume_text}
        
        JOB DESCRIPTION TEXT:
        {jd_text}
        
        CRITICAL RULES:
        1. All values for skills in ANY list must be SHORT, CONCISE KEYWORDS — maximum 3-4 words each.
        2. NEVER put full sentences or phrases as skills. Bad: "Proven working experience as a Data Analyst". Good: "Data Analysis".
        3. EXTRACT ALL SKILLS: Identify EVERY tech tool, soft skill, library, framework, and methodology from BOTH documents.
        4. DYNAMIC MATCHING: Compare the JD requirements against the Resume. Be smart (e.g., "MySQL" satisfies "SQL", "SPSS" satisfies "Statistical Analysis").
        5. required_skills must list ONLY actual skills/tools/competencies from the JD as short keywords. Do NOT include job titles, degree requirements, or experience levels.
        6. STRICT MATCHING: ONLY include a skill in "matched_skills" if there is **explicit evidence** in the resume. DO NOT assume or hallucinate soft skills or general methodologies (e.g., "Communication", "SDLC", "Agile") unless clearly mentioned or strongly proven by their points.
        7. If the resume does NOT demonstrate a required skill, it MUST go into "missing_skills". Never assume a candidate has a skill simply because it is common.
        
        Return the result in EXACT valid JSON format with these keys:
        1. "extracted_skills": Short skill keywords found in the resume.
        2. "required_skills": Short skill keywords required in the Job Description.
        3. "matched_skills": JD skills proven by the Resume.
        4. "missing_skills": JD skills NOT found in the resume.
        5. "jd_fit_score": 0-100 integer.
        6. "ats_score": 0-100 integer.
        7. "fit_level": "High Potential", "Potential Fit", or "Moderate Fit".
        8. "categorized_resume_skills": Dictionary of skill categories.
        9. "learning_paths": JSON array of items for each technical missing skill. 
           Order the array so that skills with fewer dependencies come first (adaptive sequence).
           MUST follow this EXACT nested structure for EVERY item:
           {{
             "skill": "React",
             "demand_pulse": "18k+ Openings",
             "estimated_hours": 15,
             "difficulty": "Intermediate",
             "dependencies": ["HTML", "JS Basics"],
             "status": "locked",
             "plan": [
                {{ "week": 1, "focus": "Fundamentals", "objective": "Setup env", "tasks": ["..."], "resources": ["GUVI"], "status": "not_started" }},
                {{ "week": 2, "focus": "Advanced Concepts", "objective": "Build features", "tasks": ["..."], "resources": ["Docs"], "status": "not_started" }},
                {{ "week": 3, "focus": "Deep Dive", "objective": "Complex Integrations", "tasks": ["..."], "resources": ["Coursera"], "status": "not_started" }},
                {{ "week": 4, "focus": "Deployment & Polish", "objective": "Final Project", "tasks": ["..."], "resources": ["GitHub"], "status": "not_started" }}
              ]
           }}
        10. "overall_feedback": 2 sentence professional summary highlighting the most critical gap.

        CRITICAL: Provide EXACTLY a 4-week structure for each and every skill in "learning_paths". Never provide fewer than 4 weeks.
        CRITICAL: For "resources", prioritize specialized platforms like GUVI (very important), Coursera, and Udemy.
        Return ONLY the JSON.
        """

        # models
        models_to_try = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.5-flash']
        last_error = ""

        for model_name in models_to_try:
            try:
                print(f"[AI] Trying model: {model_name}...")
                response = self.client.models.generate_content(model=model_name, contents=prompt)
                text = response.text
                text_clean = re.sub(r'```json|```', '', text).strip()
                json_match = re.search(r'\{.*\}', text_clean, re.DOTALL)
                if json_match:
                    parsed_json = json.loads(json_match.group(0))
                    raw_paths = parsed_json.get('learning_paths', [])
                    sanitized_paths = []
                    for p in raw_paths:
                        if isinstance(p, dict):
                            p['skill'] = p.get('skill', 'Technology')
                            planList = p.get('plan', [])
                            while len(planList) < 4:
                                new_week_num = len(planList) + 1
                                planList.append({
                                    "week": new_week_num,
                                    "focus": f"Week {new_week_num} Mastery",
                                    "objective": "Deep dive into advanced concepts",
                                    "tasks": ["Complete hands-on practicals", "Build a small feature"],
                                    "resources": ["GUVI", "Coursera"],
                                    "status": "not_started"
                                })
                            
                            p['plan'] = planList
                            for idx, step in enumerate(p['plan']):
                                if isinstance(step, dict):
                                    step['week'] = step.get('week', idx + 1)
                                    step['status'] = step.get('status', 'not_started')
                                    step['objective'] = step.get('objective', 'Master the core concepts.')
                                    step['tasks'] = step.get('tasks', ['Complete theoretical learning', 'Try hands-on examples'])
                                    step['resources'] = step.get('resources', ['Official Documentation'])
                            p['demand_pulse'] = p.get('demand_pulse', 'High Demand')
                            p['estimated_hours'] = p.get('estimated_hours', 10)
                            p['difficulty'] = p.get('difficulty', 'Intermediate')
                            p['status'] = p.get('status', 'available')
                            sanitized_paths.append(p)
                    
                    parsed_json['learning_paths'] = sanitized_paths
                    parsed_json['success'] = True
                    return parsed_json
            except Exception as e:
                last_error = str(e)
                print(f"[AI] Model {model_name} failed: {last_error[:80]}")

        return {"success": False, "error": f"AI models failed: {last_error}"}
