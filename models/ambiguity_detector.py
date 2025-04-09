from ollama_prompting import detect_ambiguity_with_llm

'''
##EXAMPLE
vague_req = "The system should load quickly and be user-friendly."
amb_terms = ["quickly", "user-friendly"]

output = detect_ambiguity_with_llm(amb_terms)
print(output)
'''