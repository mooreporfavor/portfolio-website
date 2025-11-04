# File: api/generate-cv.py
import os
import json
import google.generativeai as genai
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # --- 1. Read the incoming request data ---
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            job_description = data.get('jobDescription')

            if not job_description:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Job description is required"}).encode('utf-8'))
                return

            # --- 2. Configure the Gemini API ---
            # It will automatically use the GEMINI_API_KEY from Vercel's environment variables
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set.")
            genai.configure(api_key=api_key)

            # --- 3. Read the CVvault knowledge base ---
            # This robust path works on Vercel's servers
            cv_path = os.path.join(os.getcwd(), 'src/data/CVvault.md')
            with open(cv_path, 'r', encoding='utf-8') as f:
                cv_vault_text = f.read()

            # --- 4. Construct the prompt ---
            prompt = f"""
            **CONTEXT:**
            Here is my master CV. It is exhaustive and contains all my professional experience, skills, and project histories.
            ---
            {cv_vault_text}
            ---

            **TASK:**
            Act as a professional career coach and expert resume writer. Your task is to generate a new, tailored CV that highlights the skills, experiences, and project outcomes from the CONTEXT that are most relevant to the following JOB DESCRIPTION.

            **Instructions:**
            - The output must be formatted in clean, readable Markdown.
            - Re-frame bullet points to use action verbs and metrics that directly address the requirements in the job description.
            - Prioritize and re-order sections or experiences to best match the target role.
            - Do not invent any information not present in the master CV context.

            **JOB DESCRIPTION:**
            ---
            {job_description}
            ---
            """

            # --- 5. Call the Gemini API ---
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)

            # --- 6. Send the successful response back to the browser ---
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"cv": response.text}).encode('utf-8'))

        except FileNotFoundError:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Internal Server Error: CVvault.md not found at expected path."}).encode('utf-8'))
        except Exception as e:
            # This catches any other error (API key issues, model errors, etc.)
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"An unexpected error occurred: {str(e)}"}).encode('utf-8'))