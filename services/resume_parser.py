import re
import io

# PDF/DOCX extraction libraries
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import docx
except ImportError:
    docx = None


class ResumeParser:
    def __init__(self):
        # Comprehensive skill database for extraction from resume
        self.skill_db = [
            # Programming Languages
            "python", "java", "javascript", "typescript", "c++", "c#", "c",
            "php", "ruby", "swift", "kotlin", "dart", "go", "rust", "scala",
            "perl", "r", "matlab", "shell", "bash", "assembly", "lua",

            # Web / Mobile
            "html", "html5", "css", "css3", "flutter", "react native",
            "react", "angular", "vue", "vue.js", "next.js", "nuxt",
            "svelte", "gatsby", "remix", "jquery",

            # Frontend Frameworks & Styling
            "bootstrap", "tailwind", "material ui", "sass", "less",
            "redux", "webpack", "babel", "vite",

            # Data Science & AI
            "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
            "scikit-learn", "sklearn", "tensorflow", "keras", "pytorch",
            "machine learning", "deep learning", "neural networks",
            "artificial intelligence", "nlp", "nltk", "spacy", "opencv",
            "computer vision", "data science", "data mining",
            "big data", "hadoop", "spark",

            # Data Tools
            "power bi", "tableau", "looker", "google data studio",
            "excel", "vlookup", "pivot tables", "google sheets",

            # Databases
            "sql", "mysql", "postgresql", "oracle", "mongodb", "firebase",
            "redis", "cassandra", "dynamodb", "sqlite", "nosql",
            "elasticsearch", "supabase", "bigquery", "snowflake",

            # Cloud & DevOps
            "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
            "jenkins", "ci/cd", "terraform", "ansible",
            "heroku", "vercel", "netlify", "linux", "ubuntu", "nginx",
            "github actions",

            # Tools & Version Control
            "git", "github", "gitlab", "bitbucket", "figma",
            "postman", "swagger", "jira", "trello",
            "maven", "gradle", "npm", "yarn",

            # IDEs & Platforms
            "jupyter notebook", "jupyter lab", "visual studio code", "vscode",
            "google colab", "colab", "android studio", "eclipse",
            "intellij", "pycharm", "netbeans", "xcode",
            "sublime text", "notepad++", "editplus",
            "turbo c", "turbo c++", "dev c++",

            # Testing
            "selenium", "playwright", "cypress", "appium",
            "junit", "pytest", "jest", "mocha", "testng",
            "manual testing", "automation testing", "api testing",
            "agile", "scrum", "kanban",

            # Engineering
            "autocad", "solidworks", "catia", "ansys", "matlab simulink",
            "revit", "staad pro", "primavera", "labview",
            "plc", "scada", "embedded systems", "vlsi", "arduino",
            "raspberry pi", "robotics", "iot", "six sigma",

            # Soft Skills
            "communication", "people management", "collaborative",
            "time management", "problem-solving", "leadership", "teamwork",
            "analytical", "critical thinking", "creativity", "adaptability",
            "presentation", "negotiation", "decision making",

            # Office
            "powerpoint", "ms office", "word",

            # CS Fundamentals
            "data structures", "algorithms", "oop", "design patterns",
            "system design", "microservices", "rest api",
            "operating systems", "computer networks", "dbms",

            # Markup / Query
            "xml", "json", "yaml", "graphql", "latex",
        ]

    def _extract_text_from_pdf(self, file_obj):
        """Extract text from PDF using pdfplumber."""
        if pdfplumber is None:
            return None
        try:
            file_bytes = file_obj.read()
            file_obj.seek(0)
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip() if text.strip() else None
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return None

    def _extract_text_from_docx(self, file_obj):
        """Extract text from DOCX using python-docx."""
        if docx is None:
            return None
        try:
            file_bytes = file_obj.read()
            file_obj.seek(0)
            doc = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            return text.strip() if text.strip() else None
        except Exception as e:
            print(f"DOCX extraction error: {e}")
            return None

    def _extract_skills(self, text):
        """Extract skills from resume text by matching against skill database."""
        text_lower = text.lower()
        found_skills = []
        for skill in self.skill_db:
            # Use word boundary regex for accurate matching
            pattern = r'(?:^|[\s,;(|/])' + re.escape(skill) + r'(?:[\s,;)|/]|$)'
            if re.search(pattern, text_lower):
                found_skills.append(skill.upper())
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for s in found_skills:
            if s not in seen:
                seen.add(s)
                unique_skills.append(s)
        return unique_skills

    def _extract_name(self, text):
        """Try to extract name from first few lines of resume."""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if lines:
            first_line = lines[0]
            # If first line is short and doesn't look like a header, it's likely the name
            if len(first_line) < 50 and not any(kw in first_line.lower() for kw in ['resume', 'cv', 'curriculum', 'objective', 'summary']):
                return first_line
        return "Candidate"

    def _extract_email(self, text):
        """Extract email from resume text."""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        return match.group(0) if match else "not-provided@example.com"

    def _extract_phone(self, text):
        """Extract phone number from resume text."""
        # Common pattern that supports international, space separated, dashes etc.
        phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else "Not provided"

    def parse_resume(self, file_path_or_obj):
        """
        Parse resume from uploaded file (PDF or DOCX).
        Extracts text, then finds skills by matching against skill database.
        """
        raw_text = None
        filename = ""

        # Get filename
        if hasattr(file_path_or_obj, 'filename'):
            filename = file_path_or_obj.filename.lower()
        elif hasattr(file_path_or_obj, 'name'):
            filename = file_path_or_obj.name.lower()

        # Extract text based on file type
        if filename.endswith('.pdf'):
            raw_text = self._extract_text_from_pdf(file_path_or_obj)
        elif filename.endswith('.docx'):
            raw_text = self._extract_text_from_docx(file_path_or_obj)
        elif filename.endswith('.txt'):
            try:
                raw_text = file_path_or_obj.read().decode('utf-8', errors='ignore')
                file_path_or_obj.seek(0)
            except Exception:
                raw_text = None

        # If extraction failed
        if not raw_text:
            return {"error": "Could not extract text from resume. Please upload a valid PDF or DOCX file."}

        # Extract information
        extracted_skills = self._extract_skills(raw_text)
        name = self._extract_name(raw_text)
        email = self._extract_email(raw_text)
        phone = self._extract_phone(raw_text)

        if not extracted_skills:
            return {
                "name": name,
                "email": email,
                "phone": phone,
                "skills": [],
                "raw_text": raw_text,
                "warning": "No skills could be detected. Please ensure your resume contains relevant technical skills."
            }

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": extracted_skills,
            "raw_text": raw_text
        }
