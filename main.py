import os
import json
from models.github_scraper import get_requirements, save_to_file
from models.ambiguity_detector import load_requirements, generate_ambiguity_report, save_report
from models.clarifier import load_ambiguity_report, process_requirements, save_refined_requirements

# Input/output file paths
INPUT_FILE = "data/requirements.json"
AMBIGUITY_REPORT_FILE = "output/ambiguity_report.json"
REFINED_FILE = "output/refined_requirements.json"

def main():
    print("Scraping GitHub issues...")
    scraped_data = get_requirements()
    save_to_file(scraped_data, INPUT_FILE)  # Save scraped issues as your dataset

    print("Loading requirements...")
    requirements = load_requirements(INPUT_FILE)

    print("Running ambiguity detection...")
    ambiguity_report = generate_ambiguity_report(requirements)
    save_report(ambiguity_report, AMBIGUITY_REPORT_FILE)
    print(f"Ambiguity report saved to: {AMBIGUITY_REPORT_FILE}")

    print("Clarifying vague requirements...")
    loaded_report = load_ambiguity_report(AMBIGUITY_REPORT_FILE)
    refined = process_requirements(loaded_report)
    save_refined_requirements(refined, REFINED_FILE)
    print(f"Refined requirements saved to: {REFINED_FILE}")

if __name__ == "__main__":
    main()