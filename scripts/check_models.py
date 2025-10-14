# scripts/check_models.py

import google.generativeai as genai

# Use the same path to your API key
GEMINI_API_KEY_FILE = '../secrets/gemini_api_key_portfolio-website.txt'

try:
    with open(GEMINI_API_KEY_FILE, 'r') as f:
        api_key = f.read().strip()
    
    genai.configure(api_key=api_key)

    print("Available Gemini Models:")
    for model in genai.list_models():
        # We only care about models that support the 'generateContent' method
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")

except Exception as e:
    print(f"An error occurred: {e}")