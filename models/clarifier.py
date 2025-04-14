'''
#clarification script
Then Chase, you can build the clarification script.
It will read from that ambiguity report, and for any requirement marked as vague,
it will call the LLM to generate a better version, saving it to output/refined_requirements.json.

 STEP #1
 Reads output/ambiguity_report.json (from ambiguity detector)

 STEP #2
 Processes each vague requirement (where ambiguous terms were detected)

 Step #3
 Calls clarify_requirement() from ollama_prompting.py to:
       -Ask 2 clarifying questions.
       -Rewrite the requirement.

 '''


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import os
import logging
from ollama_prompting import clarify_requirement

logging.basicConfig(
    #TODO I set up this for a debug log, change file location if needed
    filename='logs/clarify.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

#TODO Change where input/output should be
INPUT_FILE = "test/ambiguity_report.json"
OUTPUT_FILE = "test/refined_requirements.json"

#load the report:

def load_ambiguity_report(filepath):
 if not os.path.exists(filepath):
  raise FileNotFoundError(f"input file not found: {filepath}")
 with open(filepath, "r", encoding="utf-8") as file:
  try:
   return json.load(file)
  except json.JSONDecodeError as e:
   raise ValueError(f"Cannot parse json: {e}")

def parse_llm_response(llm_output):
    #extract questions and rewritten requirement from LLM response string
    lines = llm_output.strip().splitlines()

    que = [line.strip('- ') for line in lines if line.strip().startswith("- Q")]
    rewritten_line = next((line for line in lines if line.strip().startswith("Rewritten Requirement:")), None)

    if not que or rewritten_line is None:
        raise ValueError("Malformed LLM response. Could not parse questions or rewritten requirement.")

    rewritten = rewritten_line.replace("Rewritten Requirement:", "").strip()
    return que, rewritten

def process_requirements(data):
    refined = []

    for entry in data:
        original = entry.get("original")
        terms = entry.get("ambiguous_terms", [])

        #skip if there's no ambiguity
        if not terms or terms == ["None"]:
            continue

        try:
            llm_output = clarify_requirement(original, terms)
            questions, rewritten = parse_llm_response(llm_output)

            refined.append({
                "original": original,
                "ambiguous_terms": terms,
                "questions": questions,
                "rewritten": rewritten
            })

        except Exception as e:
            #skip and move on
            logging.error(f"Failed to process requirement: '{original}' | Error: {str(e)}")
            continue

    return refined


def save_refined_requirements(output_data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=2)

def main():
    data = load_ambiguity_report(INPUT_FILE)
    results = process_requirements(data)
    save_refined_requirements(results, OUTPUT_FILE)


if __name__ == "__main__":
    main()