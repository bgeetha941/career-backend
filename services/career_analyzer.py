class CareerAnalyzer:
    def __init__(self):
        pass

    def evaluate_resume_against_jd(self, resume_data, jd_data):
        """
        Comprehensive comparison based on ACTUAL extracted skills from JD and Resume.
        """
        resume_skills = [s.upper() for s in resume_data.get('skills', [])]
        jd_skills = [s.upper() for s in jd_data.get('essential_skills', [])]

        if not jd_skills:
            return {"error": "Job description must contain skills to evaluate fit."}

        # Calculate exact matches
        matched_skills = [s for s in jd_skills if s in resume_skills]
        missing_skills = [s for s in jd_skills if s not in resume_skills]

        # Calculate Scores
        jd_fit_score = int((len(matched_skills) / len(jd_skills)) * 100) if jd_skills else 0
        ats_score = min(100, jd_fit_score + 15)  # Simulated ATS formatting/relevance bonus

        # Determine Fit Level
        if jd_fit_score > 80:
            fit_level = "High Potential"
        elif jd_fit_score > 40:
            fit_level = "Potential Fit"
        else:
            fit_level = "Moderate Fit"

        # Categorize Resume Skills (mapped to UI sections)
        categorized_skills = {

            "Platforms & IDEs": [s for s in resume_skills if s in [
                # Code Editors
                'VSCODE', 'VISUAL STUDIO CODE', 'SUBLIME TEXT', 'ATOM', 'NOTEPAD++',
                'EDITPLUS', 'BRACKETS', 'EMACS', 'VIM', 'NANO',
                # Full IDEs
                'ECLIPSE', 'INTELLIJ', 'INTELLIJ IDEA', 'PYCHARM', 'NETBEANS',
                'XCODE', 'ANDROID STUDIO', 'VISUAL STUDIO', 'WEBSTORM', 'PHPSTORM',
                'CLION', 'RIDER', 'GOLAND', 'DATAGRIP',
                # Data / Science IDEs
                'JUPYTER NOTEBOOK', 'JUPYTER LAB', 'GOOGLE COLAB', 'COLAB',
                'SPYDER', 'RSTUDIO', 'MATLAB',
                # Beginner IDEs
                'TURBO C', 'TURBO C++', 'DEV C++', 'CODE BLOCKS', 'CODEBLOCKS',
                # Design Tools
                'FIGMA', 'ADOBE XD', 'SKETCH', 'CANVA', 'INVISION',
            ]],

            "Languages & Frameworks": [s for s in resume_skills if s in [
                # Web Languages
                'HTML', 'HTML5', 'CSS', 'CSS3', 'JAVASCRIPT', 'TYPESCRIPT', 'PHP',
                # General Purpose
                'PYTHON', 'JAVA', 'C', 'C++', 'C#', 'GO', 'RUST',
                'RUBY', 'SCALA', 'KOTLIN', 'SWIFT', 'DART',
                # Mobile / Cross Platform
                'FLUTTER', 'REACT NATIVE',
                # Scripting / System
                'SHELL', 'BASH', 'POWERSHELL', 'PERL', 'LUA', 'GROOVY',
                # Academic / Scientific
                'R', 'MATLAB', 'ASSEMBLY', 'FORTRAN', 'COBOL',
                # Markup / Query
                'XML', 'JSON', 'YAML', 'GRAPHQL', 'LATEX', 'SPARQL',

                # Frontend Frameworks (merged from Frontend & UI)
                'REACT', 'ANGULAR', 'VUE', 'VUE.JS', 'SVELTE',
                'NEXT.JS', 'NUXT', 'GATSBY', 'REMIX',
                'REDUX', 'ZUSTAND', 'MOBX', 'CONTEXT API',
                'BOOTSTRAP', 'TAILWIND', 'MATERIAL UI', 'ANT DESIGN',
                'CHAKRA UI', 'SASS', 'LESS', 'STYLED COMPONENTS', 'BULMA',
                'WEBPACK', 'BABEL', 'VITE', 'ROLLUP', 'PARCEL',
                'JQUERY', 'RESPONSIVE DESIGN', 'CROSS-BROWSER COMPATIBILITY',
                'UI/UX', 'UX', 'UI', 'WIREFRAMING', 'PROTOTYPING',

                # Data Science & AI Libraries (merged from Data Science & AI)
                'POWER BI', 'TABLEAU', 'LOOKER', 'GOOGLE DATA STUDIO',
                'EXCEL', 'VLOOKUP', 'PIVOT TABLES', 'GOOGLE SHEETS',
                'MATPLOTLIB', 'SEABORN', 'PLOTLY', 'GGPLOT',
                'PANDAS', 'NUMPY', 'SCIPY', 'STATSMODELS', 'SCIKIT-LEARN', 'SKLEARN',
                'TENSORFLOW', 'KERAS', 'PYTORCH', 'CAFFE', 'MXNET',
                'MACHINE LEARNING', 'DEEP LEARNING', 'NEURAL NETWORKS',
                'ARTIFICIAL INTELLIGENCE', 'AI', 'ML',
                'NLTK', 'SPACY', 'BERT', 'GPT', 'TRANSFORMERS', 'HUGGINGFACE',
                'OPENCV', 'COMPUTER VISION', 'IMAGE PROCESSING',
                'DATA SCIENCE', 'DATA MINING', 'STATISTICS',
                'HYPOTHESIS TESTING', 'REGRESSION', 'CLASSIFICATION',
                'CLUSTERING', 'FEATURE ENGINEERING', 'TIME SERIES', 'FORECASTING',
                'BIG DATA', 'HADOOP', 'SPARK',
            ]],

            "Database": [s for s in resume_skills if s in [
                # Relational
                'SQL', 'MYSQL', 'POSTGRESQL', 'ORACLE', 'MS SQL', 'MSSQL',
                'SQL SERVER', 'SQLITE', 'MARIADB', 'DB2',
                # NoSQL
                'MONGODB', 'NOSQL', 'FIREBASE', 'DYNAMODB', 'CASSANDRA',
                'REDIS', 'COUCHDB', 'HBASE', 'ELASTICSEARCH', 'INFLUXDB',
                # Cloud DB / Data Warehouse
                'SUPABASE', 'PLANETSCALE', 'BIGQUERY', 'REDSHIFT', 'SNOWFLAKE',
                'HIVE', 'DATABRICKS',
                # Concepts
                'DATABASE', 'DBMS', 'RDBMS', 'NORMALIZATION',
                'STORED PROCEDURES', 'TRIGGERS', 'INDEXING', 'ER DIAGRAM',
            ]],

            "Soft Skills": [s for s in resume_skills if s in [
                # Communication
                'COMMUNICATION', 'PRESENTATION', 'PUBLIC SPEAKING',
                'REPORT WRITING', 'DOCUMENTATION', 'STORYTELLING',
                # Collaboration
                'TEAMWORK', 'COLLABORATIVE', 'INTERPERSONAL',
                'PEOPLE MANAGEMENT', 'STAKEHOLDER MANAGEMENT',
                # Thinking
                'CRITICAL THINKING', 'ANALYTICAL', 'PROBLEM-SOLVING',
                'CREATIVITY', 'INNOVATION', 'DECISION MAKING', 'LOGICAL REASONING',
                # Work Style
                'TIME MANAGEMENT', 'MULTITASKING', 'ORGANIZED',
                'ATTENTION TO DETAIL', 'SELF-MOTIVATED', 'ADAPTABILITY',
                'FLEXIBILITY', 'INITIATIVE', 'ACCOUNTABILITY',
                # Leadership
                'LEADERSHIP', 'MENTORING', 'CONFLICT RESOLUTION',
                'NEGOTIATION', 'EMOTIONAL INTELLIGENCE', 'EMPATHY',
                'COACHING', 'DELEGATION',
            ]],

            "Tools & DevOps": [s for s in resume_skills if s in [
                # Version Control
                'GIT', 'GITHUB', 'GITLAB', 'BITBUCKET', 'SVN',
                # CI/CD
                'JENKINS', 'CI/CD', 'GITHUB ACTIONS', 'CIRCLECI', 'TRAVIS CI', 'ARGOCD',
                # Containers & Orchestration
                'DOCKER', 'KUBERNETES', 'PODMAN', 'HELM',
                # Cloud
                'AWS', 'AZURE', 'GCP', 'GOOGLE CLOUD', 'CLOUD',
                'HEROKU', 'VERCEL', 'NETLIFY', 'FIREBASE HOSTING',
                # IaC / Config
                'TERRAFORM', 'ANSIBLE', 'PUPPET', 'CHEF', 'VAGRANT', 'CLOUDFORMATION',
                # Build Tools
                'MAVEN', 'GRADLE', 'NPM', 'YARN',
                # Servers / OS
                'LINUX', 'UBUNTU', 'CENTOS', 'WINDOWS SERVER', 'NGINX', 'APACHE', 'TOMCAT',
                # Monitoring
                'GRAFANA', 'PROMETHEUS', 'DATADOG', 'NEW RELIC', 'SPLUNK',
                # Productivity
                'MS OFFICE', 'WORD', 'POWERPOINT', 'NOTION', 'CONFLUENCE', 'SLACK',
            ]],

            "Testing & QA": [s for s in resume_skills if s in [
                # Test Types
                'MANUAL TESTING', 'AUTOMATION TESTING', 'AUTOMATION',
                'REGRESSION TESTING', 'LOAD TESTING', 'PERFORMANCE TESTING',
                'API TESTING', 'UAT', 'UNIT TESTING', 'INTEGRATION TESTING',
                'SMOKE TESTING', 'SANITY TESTING', 'BLACK BOX', 'WHITE BOX',
                # Web Automation
                'SELENIUM', 'PLAYWRIGHT', 'CYPRESS', 'WEBDRIVERIO',
                # Mobile Testing
                'APPIUM', 'ESPRESSO', 'XCUITEST',
                # API Tools
                'POSTMAN', 'SOAP UI', 'SWAGGER', 'INSOMNIA',
                # Test Frameworks
                'JUNIT', 'TESTNG', 'PYTEST', 'JEST', 'MOCHA', 'JASMINE', 'CUCUMBER', 'KATALON',
                # Methodologies
                'BDD', 'TDD', 'AGILE', 'SCRUM', 'KANBAN',
                # Management Tools
                'JIRA', 'TRELLO', 'ASANA', 'BUGZILLA', 'TESTRAIL', 'ZEPHYR',
            ]],

            "Core Engineering": [s for s in resume_skills if s in [
                # Design Tools
                'CAD', 'AUTOCAD', 'SOLIDWORKS', 'CATIA', 'CREO',
                'FUSION 360', 'REVIT', 'ANSYS', 'COMSOL', 'LABVIEW',
                'MATLAB SIMULINK', 'STAAD PRO', 'ETABS',
                # Mechanical Engineering
                'THERMODYNAMICS', 'FLUID MECHANICS', 'HEAT TRANSFER',
                'MECHANICS OF MACHINES', 'MATERIALS SCIENCE',
                'MANUFACTURING', 'INDUSTRIAL ENGINEERING',
                'QUALITY CONTROL', 'PRODUCTION PLANNING', 'CNC PROGRAMMING',
                'GD&T', 'HVAC', 'PIPING DESIGN', 'MECHATRONICS',
                # Civil Engineering
                'STRUCTURAL ANALYSIS', 'GEOTECHNICAL ENGINEERING',
                'TRANSPORTATION ENGINEERING', 'ENVIRONMENTAL ENGINEERING',
                'SURVEYING', 'CONSTRUCTION MANAGEMENT', 'PRIMAVERA', 'MS PROJECT',
                # Electrical / Electronics
                'POWER SYSTEMS', 'ELECTRICAL MACHINES', 'POWER ELECTRONICS',
                'CONTROL SYSTEMS', 'PLC', 'SCADA',
                'EMBEDDED SYSTEMS', 'VLSI', 'CIRCUIT DESIGN', 'PSPICE', 'MULTISIM',
                # General Engineering
                'ROBOTICS', 'IOT', 'ARDUINO', 'RASPBERRY PI',
                'MICROCONTROLLER', 'SIMULATION',
                'FINITE ELEMENT ANALYSIS', 'LEAN MANUFACTURING', 'SIX SIGMA',
            ]],

            "Fundamentals": [s for s in resume_skills if s in [
                # CS Core
                'DATA STRUCTURES', 'ALGORITHMS', 'OOP',
                'OBJECT-ORIENTED PROGRAMMING', 'FUNCTIONAL PROGRAMMING',
                'DESIGN PATTERNS', 'SYSTEM DESIGN', 'LOW LEVEL DESIGN',
                'MICROSERVICES', 'REST API', 'RESTFUL APIS', 'API DEVELOPMENT',
                # Systems
                'OPERATING SYSTEMS', 'COMPUTER NETWORKS',
                'COMPUTER ARCHITECTURE', 'MEMORY MANAGEMENT',
                'CONCURRENCY', 'MULTITHREADING',
                # Debugging & Optimization
                'DEBUGGING', 'PERFORMANCE OPTIMIZATION',
                'CODE REVIEW', 'CLEAN CODE', 'SOLID PRINCIPLES',
                # Math
                'DISCRETE MATHEMATICS', 'LINEAR ALGEBRA',
                'PROBABILITY', 'CALCULUS', 'STATISTICS',
                # SDLC / Theory
                'SOFTWARE ENGINEERING', 'SDLC',
                'SOFTWARE DEVELOPMENT LIFE CYCLE', 'WATERFALL',
            ]],
        }

        # Catch-all for any skills not in the above categories
        already_categorized = set()
        for skills in categorized_skills.values():
            already_categorized.update(skills)

        other_skills = [s for s in resume_skills if s not in already_categorized]
        if other_skills:
            categorized_skills["Additional Expertise"] = other_skills

        # Clean empty categories
        categorized_skills = {k: v for k, v in categorized_skills.items() if v}

        # Generate Learning Paths for Missing Skills
        soft_skills_list = [
            'COMMUNICATION', 'PRESENTATION', 'PUBLIC SPEAKING', 'REPORT WRITING', 
            'DOCUMENTATION', 'STORYTELLING', 'TEAMWORK', 'COLLABORATIVE', 
            'INTERPERSONAL', 'PEOPLE MANAGEMENT', 'STAKEHOLDER MANAGEMENT', 
            'CRITICAL THINKING', 'ANALYTICAL', 'PROBLEM-SOLVING', 'CREATIVITY', 
            'INNOVATION', 'DECISION MAKING', 'LOGICAL REASONING', 'TIME MANAGEMENT', 
            'MULTITASKING', 'ORGANIZED', 'ATTENTION TO DETAIL', 'SELF-MOTIVATED', 
            'ADAPTABILITY', 'FLEXIBILITY', 'INITIATIVE', 'ACCOUNTABILITY', 
            'LEADERSHIP', 'MENTORING', 'CONFLICT RESOLUTION', 'NEGOTIATION', 
            'EMOTIONAL INTELLIGENCE', 'EMPATHY', 'COACHING', 'DELEGATION'
        ]
        
        learning_paths = []
        for skill in missing_skills:
            if skill.upper() not in soft_skills_list:
                s_name = skill.title()
                learning_paths.append({
                    "skill": s_name,
                    "estimated_hours": 15 if len(s_name) > 5 else 8,
                    "difficulty": "Intermediate" if len(s_name) > 5 else "Beginner",
                    "dependencies": [],
                    "plan": [
                        {
                            "week": 1, 
                            "focus": f"Mastering {s_name} Basics",
                            "objective": "Understand the core concepts of " + s_name,
                            "tasks": ["Watch introductory tutorials", "Read official documentation"],
                            "resources": [f"Introduction to {s_name} - YouTube", f"Official {s_name} Documentation"],
                            "status": "not_started"
                        },
                        {
                            "week": 2, 
                            "focus": f"Advanced {s_name} Projects",
                            "objective": "Build hands-on practical features",
                            "tasks": ["Code along with advanced guide", "Clone a repository and experiment"],
                            "resources": [f"{s_name} Implementation Guide", "GitHub Practice Repo"],
                            "status": "not_started"
                        },
                        {
                            "week": 3, 
                            "focus": f"Deep Dive into {s_name}",
                            "objective": "Master complex integrations",
                            "tasks": ["Build a small integration", "Read expert articles on Medium"],
                            "resources": [f"Advanced {s_name} - Coursera", "GUVI Complete Course"],
                            "status": "not_started"
                        },
                        {
                            "week": 4, 
                            "focus": "Deployment & Polish",
                            "objective": "Finalize and deploy project",
                            "tasks": ["Deploy project to cloud environment", "Prepare portfolio README"],
                            "resources": ["Vercel Docs", "GitHub Actions"],
                            "status": "not_started"
                        }
                    ]
                })

        # Provide a generic, professional summary for the fallback
        feedback = f"Based on our evaluation, your resume shows a {fit_level} for this role. "
        if matched_skills:
            feedback += f"You have strong skills in {', '.join(list(matched_skills)[:3])}. "
        if missing_skills:
            feedback += f"We recommend focusing on gaining expertise in {', '.join(list(missing_skills)[:3])} to improve your fit."

        return {
            "success": True,
            "jd_fit_score": jd_fit_score,
            "ats_score": ats_score,
            "fit_level": fit_level,
            "categorized_resume_skills": categorized_skills,
            "required_skills": jd_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "learning_paths": learning_paths,
            "overall_feedback": feedback
        }

    def analyze_resume(self, resume_data):
        return {"error": "Provide a Job Description for full analysis"}
