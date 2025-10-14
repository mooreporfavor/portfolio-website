# scripts/analyze_interactions.py
import os
import time
import json
import pandas as pd
import random # <--- NEW: Import the random library

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter

# --- Imports for more robust waiting and error handling ---
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# --- FIX: Import the specific exceptions you want to catch ---
from selenium.common.exceptions import TimeoutException, NoSuchElementException 

# --- Configuration ---
CHROME_PROFILE_PATH = r"C:\Users\moore\AppData\Local\Google\Chrome\User Data"
REACTIONS_FILE_PATH = '../data_sources/linkedin_download/Reactions.csv'
OUTPUT_FILE_PATH = '../data_sources/interaction_analysis_results.json'
# --- NEW: File to track progress for resumability ---
PROCESSED_URLS_FILE = '../data_sources/processed_urls.txt' 
CHECKPOINT_FREQUENCY = 50

# --- NEW: Humanization Configuration ---
CHUNK_SIZE = 75  # Process 75 URLs...
BREAK_TIME_MINUTES = 10 # ...then take a 10-minute break.

def main():
    print("--- Starting LinkedIn Interaction Analysis (Resumable) ---")

    # 1. Load the source URLs
    try:
        reactions_df = pd.read_csv(REACTIONS_FILE_PATH)
        # We need to handle potential missing values in the 'Link' column
        post_urls = reactions_df['Link'].dropna().unique().tolist()
        print(f"Found {len(post_urls)} unique posts in total.")
    except Exception as e:
        print(f"Error reading reactions file: {e}")
        return

    # 2. --- UPGRADED: True Resumability Logic ---
    processed_urls = set()
    try:
        if os.path.exists(PROCESSED_URLS_FILE):
            with open(PROCESSED_URLS_FILE, 'r') as f:
                processed_urls = set(f.read().splitlines())
            print(f"Found {len(processed_urls)} previously processed URLs. They will be skipped.")
    except Exception as e:
        print(f"Could not read processed URLs file: {e}. Starting fresh.")

    # Filter out already processed URLs
    posts_to_process = [url for url in post_urls if url not in processed_urls]
    total_to_process = len(posts_to_process)
    if total_to_process == 0:
        print("All posts have already been processed. Nothing to do.")
        return
    print(f"--> Starting a new run with {total_to_process} posts remaining.")

    # Load existing results to append to
    all_author_profiles = []
    if os.path.exists(OUTPUT_FILE_PATH):
        try:
            with open(OUTPUT_FILE_PATH, 'r', encoding='utf-8') as f:
                # The output file stores aggregated counts. We need to "un-aggregate" it.
                existing_data = json.load(f)
                for item in existing_data:
                    all_author_profiles.extend([item['profileUrl']] * item['interactionCount'])
            print(f"Successfully loaded {len(all_author_profiles)} previous interactions from results file.")
        except json.JSONDecodeError:
            print("Warning: Output file is corrupted. Starting with a fresh results list.")
            all_author_profiles = []
    
    # 3. Set up Selenium
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--profile-directory=Default") 

    print("Initializing Chrome driver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(20) # Set a reasonable page load timeout
    print("Driver initialized successfully.")

    # You might not need this anymore if your profile is saved, but it's safe to keep.
    # If the browser opens and is already logged in, just press Enter immediately.
    print("="*50)
    print("ACTION REQUIRED: Browser is open. If not logged in, please log in now.")
    print("Press Enter to continue once you are logged in.")
    print("="*50)
    input("Press Enter to continue...")
    
    # 4. Main processing loop
    print("\n--- Starting Scraping ---")
    processed_in_chunk = 0 # --- NEW: Counter for our chunks
    for i, url in enumerate(posts_to_process):
        try:
            # --- NEW: Randomized delay before every navigation ---
            # This simulates a human pausing to "read" or think.
            time.sleep(random.uniform(4, 9))
            
            driver.get(url)
            wait = WebDriverWait(driver, 10)

            actor_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.update-components-actor__meta-link")))
            author_url = actor_element.get_attribute('href').split('?')[0]
            author_name_element = actor_element.find_element(By.CSS_SELECTOR, "span.update-components-actor__title")
            raw_author_name = author_name_element.text.strip()
            name_only = raw_author_name.split('\n')[0]
            author_name = name_only.split('•')[0].strip()
            
            if author_name and author_url:
                all_author_profiles.append(author_url)
                print(f"({i+1}/{total_to_process}) Success: Scraped post by '{author_name}'")
                
                with open(PROCESSED_URLS_FILE, 'a') as f:
                    f.write(url + '\n')
                
                processed_in_chunk += 1 # Increment our chunk counter

            # --- NEW: Logic to take a long break between chunks ---
            if processed_in_chunk >= CHUNK_SIZE:
                print(f"\n--- CHUNK COMPLETE: Processed {processed_in_chunk} URLs. ---")
                print(f"--- Taking a {BREAK_TIME_MINUTES}-minute break to appear more human. ---")
                time.sleep(BREAK_TIME_MINUTES * 60)
                print("--- Break over. Resuming scraping. ---\n")
                processed_in_chunk = 0 # Reset the counter for the next chunk

        except (TimeoutException, NoSuchElementException) as e:
            # This block now correctly catches the most common, non-fatal errors
            print(f"({i+1}/{total_to_process}) Info: Skipping {url}. Reason: {type(e).__name__}")
            # --- NEW: We should also log this as "processed" so we don't try it again ---
            with open(PROCESSED_URLS_FILE, 'a') as f:
                f.write(url + '\n')
            continue
        except Exception as e:
            print(f"({i+1}/{total_to_process}) An unexpected error occurred: {type(e).__name__}. Stopping script.")
            break

    driver.quit()

    # 5. Final Save (no changes here)
    if not all_author_profiles:
        print("\n--- Analysis Complete ---")
        print("No new author profiles were extracted.")
        return

    interaction_counts = Counter(all_author_profiles)
    top_interactions = interaction_counts.most_common(20)
    results = [{"profileUrl": profile_url, "interactionCount": count} for profile_url, count in top_interactions]
    with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print("\n--- Analysis Complete! ---")
    print(f"Final top 20 interacted-with profiles saved to: {OUTPUT_FILE_PATH}")

if __name__ == '__main__':
    main()