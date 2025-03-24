import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    """Sets up the Chrome WebDriver."""
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def send_dm_from_profile(driver, username, message):
    """Sends a direct message to an Instagram user by visiting their profile."""
    try:
        driver.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.uniform(5, 8))

        # Click "Message" button - try multiple possible selectors
        message_button = None
        possible_selectors = [
            "//button[contains(text(), 'Message')]",
            "//div[contains(text(), 'Message')]",
            "//div[@role='button'][contains(text(), 'Message')]",
        ]

        for selector in possible_selectors:
            try:
                message_button = driver.find_element(By.XPATH, selector)
                if message_button.is_displayed():
                    message_button.click()
                    break
            except:
                continue

        if not message_button:
            print(f"Message button not found for {username}")
            return

        time.sleep(random.uniform(3, 5))

        # Find and interact with message input
        try:
            # Try multiple possible message input selectors
            message_input = None
            input_selectors = [
                "//div[@role='textbox']",
                "//textarea[@placeholder='Message...']",
                "//div[contains(@class, 'focus-visible')]",
            ]

            for selector in input_selectors:
                try:
                    message_input = driver.find_element(By.XPATH, selector)
                    if message_input.is_displayed():
                        break
                except:
                    continue

            if message_input:
                # Click to focus
                message_input.click()
                time.sleep(1)
                
                # Clear any existing text and type the message
                message_input.clear()
                message_input.send_keys(message)
                time.sleep(1)

                # Send keys to trigger the send button
                message_input.send_keys(Keys.RETURN)
                time.sleep(2)

                print(f"Message sent to {username}")
            else:
                print(f"Message input not found for {username}")

        except Exception as e:
            print(f"Error sending message to {username}: {str(e)}")

    except Exception as e:
        print(f"Error accessing profile {username}: {str(e)}")


def process_excel_and_send_dms_profile_visit(file_path, message):
    """Reads usernames from an Excel file and sends DMs by visiting profiles."""
    try:
        df = pd.read_excel(file_path)
        usernames = df["Usernames"].tolist()

        driver = setup_driver()
        driver.get("https://www.instagram.com/")
        print("Please log in to Instagram in the opened browser.")

        while input("Have you already logged in? (yes/no): ").strip().lower() != "yes":
            print("Please log in and then type 'yes' to continue.")

        for username in usernames:
            if username and str(username).strip():
                send_dm_from_profile(driver, str(username).strip(), message)
                time.sleep(random.uniform(5, 10))
            else:
                print(f"Skipping invalid username: {username}")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    input_file = input("Enter the path to the Excel file containing usernames: ")
    message = input("Enter the message you want to send: ")
    process_excel_and_send_dms_profile_visit(input_file, message)

