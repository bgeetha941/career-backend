import re

class JobDescriptionParser:
    def __init__(self):
        # A vastly expanded multi-domain skill database to handle "any" JD
        self.skill_db = {
            "Development": [
                "java", "python", "c\\+\\+", "c#", "ruby", "php", "go", "rust", "javascript", "typescript",
                "spring boot", "django", "flask", "laravel", "react", "angular", "vue", "flutter", "dart",
                "node", "express", "hibernate", "restful", "graphql", "html", "css", "redux", "webpack", "babel"
            ],
            "Data & AI": [
                "sql", "nosql", "mysql", "mongodb", "postgresql", "oracle", "redis", "r", "pandas", "numpy",
                "machine learning", "data science", "nlp", "deep learning", "tableau", "power bi",
                "excel", "google data studio", "vlookup", "pivot tables", "hadoop", "spark"
            ],
            "Testing & QA": [
                "selenium", "playwright", "cypress", "postman", "jira", "manual testing", "automation",
                "unit testing", "scrum", "agile", "cucumber", "testrail", "appium", "jmeter", "soapui", "qa"
            ],
            "DevOps & Cloud": [
                "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "github", "gitlab",
                "cicd", "terraform", "ansible", "linux", "bash", "shell", "maven", "gradle"
            ],
            "Mechanical & Core": [
                "cad", "solidworks", "autocad", "thermodynamics", "fluid mechanics", "materials science",
                "manufacturing", "catia", "ansys", "matlab", "robotics", "mechanical engineering"
            ],
            "Soft Skills": [
                "communication", "people management", "collaborative", "time management", "leadership",
                "problem-solving", "analytical", "independent", "critical thinking", "presentation",
                "attention to detail", "team collaboration"
            ],
            "Fundamentals": [
                "data structures", "algorithms", "object-oriented programming", "oop", "debugging",
                "performance optimization", "hooks", "virtual dom", "es6"
            ]
        }
        
        # Skill aliases for normalization
        self.aliases = {
            "react.js": "react",
            "reactjs": "react",
            "html5": "html",
            "css3": "css",
            "es6+": "es6",
            "js": "javascript",
            "ci/cd": "cicd",
            "cloud computing": "cloud",
            "rest api": "restful",
            "restful services": "restful"
        }
        
        # Flatten the database for easy searching
        self.all_keywords = [item for sublist in self.skill_db.values() for item in sublist]

    def parse_jd(self, jd_text):
        """
        Extract skills from JD text using an exhaustive keyword scan.
        """
        # Normalize text: keep slashes for ci/cd but remove other noise
        text = jd_text.lower()
        extracted_skills = []
        
        # Check aliases first (higher priority for mixed terms like CI/CD)
        for alias, formal in self.aliases.items():
            if alias in text:
                extracted_skills.append(formal.upper())

        for skill in self.all_keywords:
            # Match whole words or phrases. 
            # Match whole words or phrases without crashing Python's re module.
            # We use negative lookbehind/lookahead to ensure the skill is not part of another word.
            pattern = rf'(?i)(?<![a-z0-9/]){re.escape(skill)}(?![a-z0-9/])'
            if re.search(pattern, text):
                extracted_skills.append(skill.upper())
        
        # Add 'CI/CD' explicitly if 'CICD' was normalized
        if "CICD" in extracted_skills:
            extracted_skills.remove("CICD")
            extracted_skills.append("CI/CD")

        # Remove duplicates
        extracted_skills = list(dict.fromkeys(extracted_skills))

        # Basic fallback to ensure something is always returned
        if not extracted_skills:
            if "react" in text: extracted_skills = ["REACT", "JAVASCRIPT", "HTML", "CSS"]

        return {
            "job_title": self._extract_title(text),
            "essential_skills": extracted_skills,
            "raw_text": jd_text
        }

    def _extract_title(self, text):
        match = re.search(r'job title:\s*(.*)', text)
        if match:
            return match.group(1).strip().title()
        
        if "react" in text: return "Frontend React Developer"
        if "qa" in text or "test" in text: return "QA Automation Engineer"
        if "data" in text: return "Data Analyst"
        return "Software Professional"
