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



import json
import os
import logging
from ollama_prompting import clarify_requirement

logging.basicConfig(
    filename='logs/clarify.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

INPUT_FILE = "output/ambiguity_report.json"
OUTPUT_FILE = "output/refined_requirements.json"

#load the report:

def load_ambiguity_report(filepath):
 if not os.path.exists(filepath):
  raise FileNotFoundError(f"Input file not found: {filepath}")
 with open(filepath, "r", encoding="utf-8") as file:
  try:
   return json.load(file)
  except json.JSONDecodeError as e:
   raise ValueError(f"Cannot parse JSON: {e}")


def main():



