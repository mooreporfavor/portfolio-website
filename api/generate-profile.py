# File: api/generate-profile.py
import os
import json
import google.generativeai as genai
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # --- 1. Read the incoming request data ---
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            user_prompt = data.get('user_prompt')

            if not user_prompt:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "User prompt is required"}).encode('utf-8'))
                return

            # Truncate user_prompt to 5000 characters
            user_prompt = user_prompt[:5000]

            # --- 2. Configure the Gemini API ---
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set.")
            genai.configure(api_key=api_key)

            # --- 3. Read the CVvault knowledge base ---
            cv_path = os.path.join(os.getcwd(), 'src/data/CVvault.md')
            with open(cv_path, 'r', encoding='utf-8') as f:
                cv_data = f.read()

            # --- 4. Construct the prompt ---
            prompt = f"""
            You are "CV Vault," an expert AI assistant for Ryan Moore. Your sole purpose is to generate professional summaries based *only* on his provided experience.
            Based on the following CV data and user prompt, generate a JSON object with a headline, summary, and skills.

            <cv_data>
            {cv_data}
            </cv_data>

            <user_prompt>
            {user_prompt}
            </user_prompt>
            """

            # --- 5. Call the Gemini API with JSON output config ---
            generation_config = {
                "response_mime_type": "application/json",
            }
            model = genai.GenerativeModel('gemini-flash-lite-latest', generation_config=generation_config)
            response = model.generate_content(prompt)

            # --- 6. Parse the response and send it ---
            try:
                profile_data = json.loads(response.text)
            except json.JSONDecodeError:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "The model did not return valid JSON."}).encode('utf-8'))
                return

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(profile_data).encode('utf-8'))

        except FileNotFoundError:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Internal Server Error: CVvault.md not found at expected path."}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"An unexpected error occurred: {str(e)}"}).encode('utf-8'))