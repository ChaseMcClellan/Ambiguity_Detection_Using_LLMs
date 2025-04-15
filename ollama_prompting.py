import requests

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_with_ollama(prompt, model=MODEL_NAME):
    """Send a prompt to Ollama and return the generated response."""
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_API, json=data)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code}, {response.text}"


def clarify_requirement(requirement, ambiguous_terms):
    """
    Given a vague requirement and list of ambiguous terms, ask the model
    to generate clarifying questions and rewrite it clearly.
    """
    terms = ", ".join(ambiguous_terms)
    prompt = f"""

    You are a software requirements analyst.

    Given the requirement below, identify any ambiguous or vague terms. Then:
    1. Ask exactly **two clarifying questions** to help refine the requirement.
    2. Rewrite the requirement to be **clearer and more specific**, using neutral, concise language.
    3. **Do not** invent extra functionality or features that were not mentioned in the original text.
    4. Do **not** assume advanced logic like roles, interfaces, dashboards, or priorities unless stated.

Original Requirement:
"{requirement}"

Ambiguous terms detected: {terms}

Please:
1. Ask 2 clarifying questions to improve the requirement.
2. Rewrite the requirement with specific details only making it more specific based on the ambiguous terms. Do not add extra functionality or assumptions.

Respond in this format:

Questions:
- Q1
- Q2

Rewritten Requirement:
<write your improved version here on this line>
"""
    return generate_with_ollama(prompt)


def detect_ambiguity_with_llm(requirement: str):
    prompt = f"""
You are an expert in software requirements analysis.

Analyze the following requirement and list any **ambiguous, vague, or subjective** terms that could be misunderstood or need clarification.
Instructions:
- ONLY return a bullet list of terms (no explanations).
- Do NOT include extra text or reasoning.
- If no ambiguous terms are found, respond with only:
Ambiguous Terms:
- None

Requirement:
"{requirement}"

Respond with just the term:
Ambiguous Terms:
- "term1"
- "term2"

Respond only with the list of ambiguous terms. Example:
["fast", "user-friendly"]

"""
    return generate_with_ollama(prompt)
