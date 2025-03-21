# dm_sender_profile_visit.py
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException


def setup_driver():
    """Sets up the Chrome WebDriver."""
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def send_dm_from_profile(driver, username, message):
    """Sends a direct message to an Instagram user by visiting their profile."""
    try:
        driver.get(f"https://www.instagram.com/{username}/")
        time.sleep(5)  # Wait for profile to load

        # Find and click the "Message" button
        message_button = driver.find_element(
            By.XPATH, "//div[contains(text(), 'Message')]"
        )
        message_button.click()
        time.sleep(3)  # Wait for message modal to load

        # Enter message
        message_box = driver.find_element(
            By.XPATH, "//textarea[@placeholder='Message...']"
        )
        message_box.send_keys(message)
        time.sleep(2)

        # Send message
        send_button = driver.find_element(By.XPATH, "//button[contains(text(),'Send')]")
        send_button.click()
        time.sleep(3)

        print(f"Message sent to {username}")

    except NoSuchElementException:
        print(f"Message button not found on {username}'s profile. Skipping.")
    except Exception as e:
        print(f"Error sending message to {username}: {e}")


def process_excel_and_send_dms_profile_visit(file_path, message):
    """Reads usernames from an Excel file and sends DMs by visiting profiles."""
    try:
        df = pd.read_excel(file_path)
        usernames = df["Usernames"].tolist()

        driver = setup_driver()
        driver.get("https://www.instagram.com/")
        print("Please log in to Instagram in the opened browser.")
        while True:
            logged_in = input("Have you already logged in? (yes/no): ").strip().lower()
            if logged_in == "yes":
                break
            elif logged_in == "no":
                print("Please log in and then type 'yes' to continue.")
            else:
                print("Invalid input. Please type 'yes' or 'no'.")

        for username in usernames:
            send_dm_from_profile(driver, username, message)
            time.sleep(5)  # Delay between profiles

        driver.quit()
        print("All messages sent (or skipped due to errors).")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    input_file = input("Enter the path to the Excel file containing usernames: ")
    message = input("Enter the message to send: ")
    process_excel_and_send_dms_profile_visit(input_file, message)

