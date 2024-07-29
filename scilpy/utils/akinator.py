
import json
import pathlib
from difflib import SequenceMatcher

def load_knowledge_base(knowledge_base_path):
    """Load the knowledge base from a JSON file."""
    with open(knowledge_base_path, 'r') as f:
        return json.load(f)

def similarity(a, b):
    """Calculate similarity between two strings."""
    return SequenceMatcher(None, a, b).ratio()

def ask_question(question):
    """Ask a question to the user and return the response."""
    response = input(question + " ")
    return response

def fuzzy_match_scripts(scripts, response, attribute):
    """Fuzzy match user response to script attributes."""
    scores = {}
    for script in scripts:
        for item in script[attribute]:
            match_score = similarity(response, item)
            if match_score > 0.5:  # threshold for fuzzy matching
                if script['name'] not in scores:
                    scores[script['name']] = 0
                scores[script['name']] += match_score
    return scores

def refine_scripts_by_category(scripts, category):
    """Refine the list of scripts based on category."""
    return [script for script in scripts if script['category'] == category]

def main():
    base_dir = pathlib.Path(__file__).parent
    knowledge_base_path = base_dir /'Vocabulary'/'knowledge_base.json'
    knowledge_base = load_knowledge_base(knowledge_base_path)
    scripts = knowledge_base['scripts']

    print("Welcome to the SCILPY script finder!")
    category = ask_question("Do you know the category of the script you're looking for?")
    if category:
        scripts = refine_scripts_by_category(scripts, category)

    questions = [
        "What is the script supposed to do?",
        "Which keywords describe the script?",
        "Any specific functionality you are looking for?"
    ]

    for question in questions:
        response = ask_question(question)
        script_scores = fuzzy_match_scripts(scripts, response, 'keywords')
        
        if script_scores:
            print("Based on your answer, here are some suggestions:")
            sorted_scripts = sorted(script_scores.items(), key=lambda item: item[1], reverse=True)
            for script_name, score in sorted_scripts[:5]:  # show top 5 matches
                print(f"Script: {script_name}, Score: {score}")
        else:
            print("No matching scripts found for this question.")

    print("Thank you for using the SCILPY script finder!")

if __name__ == "__main__":
    main()
