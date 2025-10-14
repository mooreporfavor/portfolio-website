import os
import io
import json
import pandas as pd
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from docx import Document
from pdfminer.high_level import extract_text

# --- Configuration ---
# This is the secret key file you downloaded from Google Cloud
SERVICE_ACCOUNT_FILE = '../secrets/credentials.json'

# This defines the permissions our script is asking for.
# 'drive.readonly' is safe because it only allows reading files.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CV_FOLDER_ID = '0B1XjUfdovCP4ZFI4SUw1NjZNTU0'
GEMINI_API_KEY_FILE = '../secrets/gemini_api_key.txt'
LINKEDIN_DATA_PATH = '../data_sources/'
def get_drive_service():
    """Authenticates and returns a Google Drive service object."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

# --- Module 1a: LinkedIn Data Ingestion ---
def load_linkedin_data():
    """Reads key CSV files from the LinkedIn export and formats them as text."""
    print("--- Step 1/4: Loading Structured Data from LinkedIn CSVs ---")
    formatted_text = ""
    try:
        positions_df = pd.read_csv(os.path.join(LINKEDIN_DATA_PATH, 'Positions.csv'))
        formatted_text += "LINKEDIN POSITIONS (Source of Truth for Titles/Dates):\n\n"
        for _, row in positions_df.iterrows():
            formatted_text += f"- Title: {row['Title']}\n  Company: {row['CompanyName']}\n  Date Range: {row['StartDate']} to {row.get('EndDate', 'Present')}\n\n"

        skills_df = pd.read_csv(os.path.join(LINKEDIN_DATA_PATH, 'Skills.csv'))
        formatted_text += "\nLINKEDIN SKILLS:\n" + ", ".join(skills_df['Name'].tolist()) + "\n\n"

        projects_df = pd.read_csv(os.path.join(LINKEDIN_DATA_PATH, 'Projects.csv'))
        formatted_text += "\nLINKEDIN PROJECTS:\n\n"
        for _, row in projects_df.iterrows():
            formatted_text += f"- Title: {row['Title']}\n  Date: {row['StartDate']}\n  Description: {row['Description']}\n\n"
        
        print("Successfully loaded structured LinkedIn data.")
        return formatted_text
    except FileNotFoundError as e:
        print(f"WARNING: LinkedIn CSV file not found: {e}. Proceeding with Drive data only.")
        return ""
    except Exception as e:
        print(f"An error occurred loading LinkedIn data: {e}")
        return ""

# --- Module 1b: Google Drive Data Ingestion ---
def get_drive_content():
    """Connects to Google Drive, finds all files, and extracts their text content."""
    print("--- Step 2/4: Loading Unstructured Narratives from Google Drive ---")
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)
        
        results = service.files().list(q=f"'{CV_FOLDER_ID}' in parents", pageSize=100, fields="files(id, name, mimeType)").execute()
        items = results.get('files', [])
        
        if not items: return ""

        all_text_content = ""
        processed_file_names = set()
        for item in items:
            file_name = item['name']
            if "CVvault" in file_name or file_name in processed_file_names: continue
            processed_file_names.add(file_name)

            file_id, mime_type = item['id'], item['mimeType']
            text = ""
            try:
                if mime_type == 'application/vnd.google-apps.document':
                    request = service.files().export_media(fileId=file_id, mimeType='text/plain')
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done: status, done = downloader.next_chunk()
                    text = fh.getvalue().decode()
                elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    request = service.files().get_media(fileId=file_id)
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done: status, done = downloader.next_chunk()
                    fh.seek(0)
                    document = Document(fh)
                    text = "\n".join([para.text for para in document.paragraphs])
                elif mime_type == 'application/pdf':
                    request = service.files().get_media(fileId=file_id)
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done: status, done = downloader.next_chunk()
                    fh.seek(0)
                    text = extract_text(fh)
                else: continue
                
                if len(text.strip()) > 10:
                    all_text_content += f"\n\n--- Content from: {file_name} ---\n\n" + text
            except Exception as e:
                print(f"ERROR processing {file_name}: {e}")
        
        print(f"Successfully extracted {len(all_text_content)} characters from Google Drive.")
        return all_text_content
    except Exception as e:
        print(f"An error occurred during Google Drive processing: {e}")
        return ""

# --- Module 2a: AI Synthesis (CVvault Generation) ---
def synthesize_cv_vault(combined_content):
    """Takes the combined text and uses Gemini to synthesize the master CVvault."""
    print("--- Step 3/4: Synthesizing Master CVvault with Gemini ---")
    try:
        with open(GEMINI_API_KEY_FILE, 'r') as f: api_key = f.read().strip()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro-latest')
        prompt = """
        Act as a professional career archivist. Your task is to synthesize the following career documents into a single master Curriculum Vitae ('CVvault').
        You have been given two types of information:
        1.  **Structured Data from LinkedIn:** This is the primary source of truth for job titles, company names, and dates.
        2.  **Unstructured Narratives:** These are detailed descriptions of projects and accomplishments from various documents.
        Your job is to intelligently merge these two sources. Use the structured data as the skeleton and flesh it out with the rich detail from the unstructured narratives. De-duplicate, chronologically order, and format the output in clean Markdown. Be exhaustive.
        Begin the synthesis now. Here is the combined source text:
        """
        print("Sending request to Gemini API. This may take a moment...")
        response = model.generate_content(prompt + combined_content)
        print("CVvault synthesis successful!")
        return response.text
    except Exception as e:
        print(f"An error during CVvault synthesis: {e}")
        return None

# --- Module 2b: AI Structuring (JSON Generation) ---
def generate_structured_projects(cv_vault_content):
    """Takes the CVvault text and uses Gemini to extract structured project data."""
    print("--- Step 4/4: Generating Structured Project JSON from CVvault ---")
    try:
        with open(GEMINI_API_KEY_FILE, 'r') as f: api_key = f.read().strip()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro-latest')
        prompt = """
        Act as a data extraction specialist. Your task is to analyze the provided master CV ('CVvault') and extract the 3-5 most impactful and distinct professional roles or projects. For each one, you must generate a JSON object that strictly adheres to the following schema.
        Schema:
        {
          "title": "string", "company": "string", "period": "string (e.g., '2023 - Present')",
          "summary": "string (A 1-2 sentence public-facing summary).",
          "problem": "string (The core problem or challenge addressed).",
          "methodology": ["string (A bullet point describing a key action)."],
          "outcome": "string (The specific, quantifiable outcome).",
          "skills": ["string (A list of key skills or technologies)."]
        }
        Carefully analyze the entire CV. Select only the most significant projects that best showcase a combination of technical and strategic skills. Do not invent information. Ensure the output is a single, valid JSON array containing these objects. Your entire response must be ONLY the JSON array, with no other text, explanations, or formatting.
        """
        print("Sending request to Gemini for structured data. This may take a moment...")
        response = model.generate_content(prompt + "\n\nCV VAULT CONTENT:\n" + cv_vault_content)
        cleaned_json = response.text.strip().replace('```json', '').replace('```', '')
        print("Structured data received!")
        return json.loads(cleaned_json)
    except Exception as e:
        print(f"An error occurred during structured data generation: {e}")
        return None

# --- Main Orchestrator ---
def main():
    cv_vault_content = ""
    cv_vault_path = "../CVvault_output.md"

    # Efficiency Check: If CVvault exists, use it. Otherwise, generate it.
    if os.path.exists(cv_vault_path):
        print("Found existing CVvault, reading from file to save time and API calls.")
        with open(cv_vault_path, 'r', encoding='utf-8') as f:
            cv_vault_content = f.read()
    else:
        # Step 1 & 2: Load all raw data
        linkedin_content = load_linkedin_data()
        drive_content = get_drive_content()
        combined_content = linkedin_content + "\n\n" + drive_content
        
        # Step 3: Synthesize the CVvault
        if combined_content.strip():
            cv_vault_content = synthesize_cv_vault(combined_content)
            if cv_vault_content:
                with open(cv_vault_path, 'w', encoding='utf-8') as f:
                    f.write(cv_vault_content)
                print(f"Master CVvault saved successfully to {cv_vault_path}")
        else:
            print("No content found from data sources. Halting.")
            return

    # Step 4: Generate structured projects from the CVvault
    if cv_vault_content:
        structured_projects = generate_structured_projects(cv_vault_content)
        if structured_projects:
            output_dir = "../src/data"
            os.makedirs(output_dir, exist_ok=True)
            output_filename = os.path.join(output_dir, "projects.json")
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(structured_projects, f, ensure_ascii=False, indent=2)
            print(f"\n==============================================")
            print(f"  Structured projects successfully generated!")
            print(f"  Saved to: {output_filename}")
            print("==============================================")

if __name__ == '__main__':
    main()