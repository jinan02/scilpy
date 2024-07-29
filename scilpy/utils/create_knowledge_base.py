import os
import json
import ast
import pathlib

def extract_docstring(script_path):
    """Extract a python file's docstring from a filepath."""
    with open(script_path, 'r') as reader:
        file_contents = reader.read()
    module = ast.parse(file_contents)
    docstring = ast.get_docstring(module) or ''
    return docstring

def load_keywords(keywords_file_path):
    """Load keywords from a JSON file."""
    with open(keywords_file_path, 'r') as f:
        keywords_data = json.load(f)
    return {script['name']: script['keywords'] for script in keywords_data['scripts']}

def update_knowledge_base(script_dir, keywords_file_path, knowledge_base_path):
    """Update the knowledge base with script information."""
    scripts_dir = pathlib.Path(script_dir)
    keywords_data = load_keywords(keywords_file_path)
    
    if os.path.exists(knowledge_base_path):
        with open(knowledge_base_path, 'r') as f:
            knowledge_base = json.load(f)
    else:
        knowledge_base = {"scripts": []}
    
    existing_scripts = {script['name']: script for script in knowledge_base['scripts']}
    
    
    for script_path in scripts_dir.glob('scil_*.py'):
        script_name = script_path.name
        description = extract_docstring(script_path)
        keywords = keywords_data.get(script_name, [])
        category = script_name.split('_')[1] if len(script_name.split('_')) > 1 else "unknown"
        
        script_info = {
            "name": script_name,
            "description": description,
            "keywords": keywords,
            "category": category
        }
        
        existing_scripts[script_name] = script_info
    
    knowledge_base['scripts'] = list(existing_scripts.values())
    
    with open(knowledge_base_path, 'w') as f:
        json.dump(knowledge_base, f, indent=4)

if __name__ == "__main__":
    base_dir = pathlib.Path(__file__).parent
    script_dir = base_dir.parent.parent/'scripts'
    keywords_file_path = base_dir/'Vocabulary'/'Keywords.json'
    knowledge_base_path = base_dir/'Vocabulary'/'knowledge_base.json'
    
    update_knowledge_base(script_dir, keywords_file_path, knowledge_base_path)
    print(f"Knowledge base updated and saved to {knowledge_base_path}")
