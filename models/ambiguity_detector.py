from ollama_prompting import detect_ambiguity_with_llm

'''
##EXAMPLE
vague_req = "The system should load quickly and be user-friendly."
amb_terms = ["quickly", "user-friendly"]

output = detect_ambiguity_with_llm(amb_terms)
print(output)
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import os
import logging
from ollama_prompting import detect_ambiguity_with_llm

logging.basicConfig(
    filename='logs/ambiguity.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# File paths
INPUT_FILE = "input/requirements.json"
OUTPUT_FILE = "test/ambiguity_report.json"

def load_input_requirements(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Cannot parse JSON: {e}")

def parse_llm_response(response_text):
    lines = response_text.strip().splitlines()
    terms = []

    for line in lines:
        if line.startswith("- "):
            term = line[2:].strip()
            if term.lower() != "none":
                terms.append(term)
    return terms

def process_requirements(data):
    results = []

    for entry in data:
        requirement = entry.get("requirement")
        if not requirement:
            continue

        try:
            llm_output = detect_ambiguity_with_llm(requirement)
            ambiguous_terms = parse_llm_response(llm_output)

            results.append({
                "original": requirement,
                "ambiguous_terms": ambiguous_terms
            })

        except Exception as e:
            logging.error(f"Failed to process requirement: '{requirement}' | Error: {str(e)}")
            continue

    return results

def save_ambiguity_report(output_data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=2)

def main():
    data = load_input_requirements(INPUT_FILE)
    results = process_requirements(data)
    save_ambiguity_report(results, OUTPUT_FILE)

if __name__ == "__main__":
    main()

print("✅ Ambiguity detection completed. Output written to:", OUTPUT_FILE)


