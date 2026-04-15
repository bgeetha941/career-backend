import re

path = r'c:\Users\HP\one\backend\services\ai_analyzer.py'
with open(path, 'r') as f:
    content = f.read()

# Replace the single week example with multi-week
old_plan = r'"plan": \[\s+{{.*?}}\s+\]'
new_plan = '"plan": [\n                {{ "week": 1, "focus": "Fundamentals", "objective": "Setup env", "tasks": ["..."], "resources": ["GUVI"], "status": "not_started" }},\n                {{ "week": 2, "focus": "Advanced Concepts", "objective": "Build features", "tasks": ["..."], "resources": ["Docs"], "status": "not_started" }},\n                {{ "week": 3, "focus": "Deployment", "objective": "Final Project", "tasks": ["..."], "resources": ["GitHub"], "status": "not_started" }}\n              ]'

content = re.sub(old_plan, new_plan, content, flags=re.DOTALL)

with open(path, 'w') as f:
    f.write(content)

print("Update complete")
