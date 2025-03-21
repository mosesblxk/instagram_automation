from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
import re
from bs4 import BeautifulSoup
import os
from datetime import datetime
fom datetime import datetime


def setup_driver():
    """
    Sets up the Chrome WebDriver with the necessary options.
    Returns:
        WebDriver: The configured Chrome WebDriver instance.
    """
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def extract_location_from_text(text):
    """
    Attempt to extract location information from text using various patterns.
    """
    location_patterns = [
        r"📍\s*([\w\s,]+)",  # Location pin emoji followed by text
        r"📌\s*([\w\s,]+)",  # Another common location pin
        r"Location[:\s]+(\w[\w\s,]+)",  # "Location:" followed by text
        r"Based in[:\s]+(\w[\w\s,]+)",  # "Based in" followed by text
        r"Living in[:\s]+(\w[\w\s,]+)",  # "Living in" followed by text
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z]{2})",  # City, State format
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z][a-z]+)",  # City, Country format
    ]

    found_locations = []
    for pattern in location_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            found_locations.append(match.group(1).strip())

    return found_locations if found_locations else None


def get_recent_post_locations(driver, num_posts=3):
    """
    Get locations from recent posts.
    """
    locations = []
    try:
        # Find post elements
        posts = driver.find_elements(By.CSS_SELECTOR, "article a")

        for post in posts[:num_posts]:
            try:
                post.click()
                time.sleep(2)

                # Try to find location
                location_element = driver.find_element(
                    By.CSS_SELECTOR, "a[href*='/explore/locations/']"
                )
                if location_element:
                    locations.append(location_element.text)

                # Close post
                close_button = driver.find_element(
                    By.CSS_SELECTOR, "button[aria-label='Close']"
                )
                close_button.click()
                time.sleep(1)

            except Exception as e:
                print(f"Error processing post: {e}")
                continue

    except Exception as e:
        print(f"Error getting post locations: {e}")

    return locations


def extract_profile_info(driver, username):
    """
    Visits a profile and extracts detailed information.
    """
    try:
        profile_url = f"https://www.instagram.com/{username}/"
        driver.get(profile_url)
        time.sleep(2)

        profile_info = {
            "username": username,
            "bio": "",
            "website": "",
            "external_links": [],
            "full_name": "",
            "followed_by": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Get bio and website
        try:
            bio_container = driver.find_element(By.CSS_SELECTOR, "div.x7a106z")

            # Get bio text
            try:
                bio_element = bio_container.find_element(
                    By.CSS_SELECTOR, "span._ap3a._aaco._aacu._aacx._aad7._aade"
                )
                profile_info["bio"] = bio_element.text
            except:
                pass

            # Get website
            try:
                website_element = bio_container.find_element(
                    By.CSS_SELECTOR, "div.x3nfvp2 a"
                )
                profile_info["website"] = website_element.get_attribute("href")
            except:
                pass

            # Get external links (like Threads)
            try:
                external_links = bio_container.find_elements(
                    By.CSS_SELECTOR, "div.x1dc814f a"
                )
                for link in external_links:
                    link_text = link.text
                    link_url = link.get_attribute("href")
                    if link_text and link_url:
                        profile_info["external_links"].append({
                            "platform": link_text,
                            "url": link_url,
                        })
            except:
                pass

            # Get followed by information
            try:
                followed_by = bio_container.find_elements(
                    By.CSS_SELECTOR, "span.x5n08af"
                )
                profile_info["followed_by"] = [
                    elem.text for elem in followed_by if elem.text
                ]
            except:
                pass

        except Exception as e:
            print(f"Error extracting bio container info: {e}")

        return profile_info

    except Exception as e:
        print(f"Error accessing profile {username}: {e}")
        return None


def process_profiles(input_file, output_file=None):
    """
    Process profiles from input Excel file and save results to output file.
    """
    # Read usernames from input file
    df = pd.read_excel(input_file)
    usernames = df["Usernames"].tolist()

    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = input_file.replace(".xlsx", f"_profile_info_{timestamp}.xlsx")

    driver = setup_driver()
    all_profiles = []
    total = len(usernames)

    # Create backup folder if it doesn't exist
    backup_folder = "profile_scraping_backups"
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    try:
        # Login prompt
        print("Please log in to Instagram in the opened browser.")
        driver.get("https://www.instagram.com/")
        while True:
            logged_in = input("Have you logged in? (yes/no): ").strip().lower()
            if logged_in == "yes":
                break
            time.sleep(1)

        # Load existing progress if any
        if os.path.exists(output_file):
            existing_df = pd.read_excel(output_file)
            all_profiles = existing_df.to_dict("records")
            processed_usernames = set(existing_df["username"].tolist())
            print(f"Loaded {len(all_profiles)} profiles from existing file")
        else:
            processed_usernames = set()

        for idx, username in enumerate(usernames, 1):
            if username in processed_usernames:
                print(f"Skipping already processed profile {idx}/{total}: {username}")
                continue

            print(f"\nProcessing profile {idx}/{total}: {username}")

            # Extract profile info
            profile_info = extract_profile_info(driver, username)

            if profile_info:
                all_profiles.append(profile_info)

                # Save progress every 5 profiles
                if idx % 5 == 0:
                    # Save to main file
                    df_profiles = pd.DataFrame(all_profiles)
                    df_profiles.to_excel(output_file, index=False)

                    # Save backup
                    backup_file = os.path.join(
                        backup_folder, f"backup_{timestamp}_profiles_{idx}.xlsx"
                    )
                    df_profiles.to_excel(backup_file, index=False)

                    print(f"Progress saved. Processed {idx}/{total} profiles")
                    print(f"Backup created: {backup_file}")

            # Add random delay to prevent rate limiting
            time.sleep(random.uniform(3, 5))

            # Take a longer break every 50 profiles
            if idx % 50 == 0:
                print("Taking a break to prevent rate limiting...")
                time.sleep(30)

        # Final save
        df_profiles = pd.DataFrame(all_profiles)
        df_profiles.to_excel(output_file, index=False)

        # Final backup
        final_backup = os.path.join(
            backup_folder, f"final_backup_{timestamp}_complete.xlsx"
        )
        df_profiles.to_excel(final_backup, index=False)

        print("\nAll profiles processed and saved!")
        print(f"Output file: {output_file}")
        print(f"Final backup: {final_backup}")

    except Exception as e:
        print(f"An error occurred: {e}")

        # Emergency save on error
        if all_profiles:
            df_profiles = pd.DataFrame(all_profiles)
            error_file = os.path.join(backup_folder, f"error_recovery_{timestamp}.xlsx")
            df_profiles.to_excel(error_file, index=False)
            print(f"Emergency backup saved to: {error_file}")

    finally:
        driver.quit()


if __name__ == "__main__":
    input_file = input("Enter the path to your Excel file containing usernames: ")
    process_profiles(input_file)

