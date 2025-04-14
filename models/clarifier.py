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
from ollama_prompting import clarify_requirement

#load the report:

with open("output/ambiguity_report.json", "r") as file:
  ambiguity_report = json.load(file)

refined_output = []

for item in ambiguity_report:
 og = item["original"]
 amTerm = item["ambiguous_terms"]
 if amTerm and amTerm !=["None"]:
  result = clarify_requirement(og, amTerm)

  #split the result into quesions and rewrite
  lines = result.strip().splitlines()
  questions = [line.strip() for line in lines if line.startswith("- Q")]
  rewritten = next((line for line in lines if line.startswith("Rewritten Requirements")), None)


