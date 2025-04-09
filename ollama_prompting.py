import requests

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


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
Original Requirement:
"{requirement}"

Ambiguous terms detected: {terms}

Please:
1. Ask 2 clarifying questions to improve the requirement.
2. Rewrite the requirement with specific details.

Respond in this format:

Questions:
- Q1
- Q2

Rewritten Requirement:
<your improved version>
"""
    return generate_with_ollama(prompt)

def detect_ambiguity_with_llm(requirement: str):
    prompt = f"""
You are an expert in software requirements analysis.

Analyze the following requirement and list any **ambiguous, vague, or subjective** terms that could be misunderstood or need clarification.

Requirement:
"{requirement}"

Respond with:
Ambiguous Terms:
- term1
- term2

If the requirement is clear, just respond:
Ambiguous Terms:
- None
"""
    return generate_with_ollama(prompt)
