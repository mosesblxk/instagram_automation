from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
import time


def setup_driver():
    """
    Sets up the Chrome WebDriver with the necessary options.
    Returns:
        WebDriver: The configured Chrome WebDriver instance.
    """
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def open_url(driver, url):
    """
    Opens the Instagram profile URL using the provided WebDriver.
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        url (str): The URL of the Instagram profile to open.
    """
    driver.get(url)


def get_follower_count(driver):
    """
    Gets the total follower count from the profile page.
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
    Returns:
        int: The number of followers, or None if count cannot be determined.
    """
    try:
        time.sleep(2)  # Wait for the count to load
        count_element = driver.find_element(
            By.XPATH, "//a[contains(@href, '/followers')]/span"
        )
        count_text = count_element.get_attribute("title") or count_element.text
        return int(count_text.replace(",", ""))
    except Exception as e:
        print(f"Error getting follower count: {e}")
        return None


def click_list_button(driver, list_type):
    """
    Clicks the 'followers' or 'following' button on the Instagram profile page.
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        list_type (str): Either 'followers' or 'following'.
    """
    try:
        if list_type == "followers":
            button_xpath = "//a[contains(@href, '/followers')]"
        elif list_type == "following":
            button_xpath = "//a[contains(@href, '/following')]"
        else:
            raise ValueError("list_type must be 'followers' or 'following'")

        following_link = driver.find_element(By.XPATH, button_xpath)
        driver.execute_script("arguments[0].click();", following_link)
        time.sleep(4)  # Wait for the modal to open
    except Exception as e:
        print(f"Error clicking {list_type} button: {e}")
        raise


def get_accountlist_div_name(driver):
    """
    Identifies and retrieves the class name of the div containing the list of accounts.
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
    Returns:
        str: The class name of the div element that contains the list of accounts.
    """
    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        accountlist_div_name = None
        for div in soup.find_all("div", style=True):
            if div.get("style") == "height: auto; overflow: hidden auto;":
                accountlist_div_name = div.find_parent("div").get("class")[0]
                break
        if not accountlist_div_name:
            print("Warning: Could not find account list div name")
        return accountlist_div_name
    except Exception as e:
        print(f"Error getting account list div name: {e}")
        return None


def extract_currently_visible_usernames(account_list):
    """
    Extracts usernames that are currently visible in the account list.
    Args:
        account_list (WebElement): The account list WebElement.
    Returns:
        set: A set of unique Instagram usernames currently visible.
    """
    try:
        accountlist_html = account_list.get_attribute("outerHTML")
        soup = BeautifulSoup(accountlist_html, "html.parser")

        # Find all account links and extract the usernames
        account_links = soup.find_all("a", href=True)
        usernames = set()

        for link in account_links:
            href = link["href"].strip("/")
            # Only include usernames, not other links
            if (
                "/" not in href
                and href != ""
                and not href.startswith(("explore", "p/", "reels", "stories"))
            ):
                usernames.add(href)

        return usernames
    except Exception as e:
        print(f"Error extracting usernames: {e}")
        return set()


def incremental_scroll_and_save(
    driver,
    accountlist_div_name,
    file_path,
    expected_count=None,
    scroll_delay=3.0,
    save_interval=10,
):
    """
    Scrolls through the account list and saves usernames incrementally.
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        accountlist_div_name (str): The class name of the account list div.
        file_path (str): Path to save the Excel file.
        expected_count (int): Expected number of followers/following.
        scroll_delay (float): Time to wait between scrolls.
        save_interval (int): Number of scrolls before saving to file.
    Returns:
        list: A complete list of unique Instagram usernames.
    """
    try:
        account_list = driver.find_element(By.CLASS_NAME, accountlist_div_name)
        all_usernames = set()
        previous_count = 0
        scroll_count = 0
        consecutive_same_count = 0

        print("Starting to scroll and collect usernames...")

        # Get initial scroll height
        last_height = driver.execute_script(
            "return arguments[0].scrollHeight", account_list
        )

        while True:
            # Extract usernames currently visible
            new_usernames = extract_currently_visible_usernames(account_list)
            all_usernames.update(new_usernames)

            # Print progress
            current_count = len(all_usernames)
            if current_count > previous_count:
                print(f"Found {current_count} unique usernames so far...")
                previous_count = current_count
                consecutive_same_count = 0
            else:
                consecutive_same_count += 1

            # Check if we've reached expected count
            if expected_count and len(all_usernames) >= expected_count * 0.95:
                print("Reached 95% of expected count. Finishing...")
                break

            # Scroll down
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", account_list
            )
            time.sleep(scroll_delay)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(
                "return arguments[0].scrollHeight", account_list
            )

            # If heights are the same and no new usernames in last 10 attempts, exit
            if new_height == last_height and consecutive_same_count > 10:
                print("No new content loaded after multiple attempts. Finishing...")
                break

            last_height = new_height
            scroll_count += 1

            # Save incrementally
            if scroll_count % save_interval == 0:
                save_progress_to_excel(list(all_usernames), file_path)
                print(f"Progress saved: {len(all_usernames)} usernames")

            # Add a longer pause every 50 scrolls to prevent rate limiting
            if scroll_count % 50 == 0:
                print("Taking a short break to prevent rate limiting...")
                time.sleep(5)

    except Exception as e:
        print(f"Error while scrolling: {e}")
        return list(all_usernames)

    # Final save
    all_usernames_list = list(all_usernames)
    save_progress_to_excel(all_usernames_list, file_path)
    print(f"Completed! Total usernames collected: {len(all_usernames_list)}")

    return all_usernames_list


def save_progress_to_excel(usernames, file_path):
    """
    Saves the current list of usernames to an Excel file.
    Args:
        usernames (list): List of usernames to save.
        file_path (str): Path to save the Excel file.
    """
    try:
        df = pd.DataFrame(usernames, columns=["Usernames"])
        df.to_excel(file_path, index=False)
    except Exception as e:
        print(f"Error saving to Excel: {e}")


def select_save_file():
    """
    Prompts the user to select a file path to save the results.
    Returns:
        str: The selected file path.
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
        title="Save Instagram Usernames",
    )
    return file_path


def main():
    """
    Main function that orchestrates the process of scraping Instagram followers or following.
    """
    profile_id = input("Enter the Instagram profile ID: ")
    while True:
        list_type = (
            input("Do you want to extract 'followers' or 'following'?: ")
            .strip()
            .lower()
        )
        if list_type in ["followers", "following"]:
            break
        else:
            print("Invalid input. Please type 'followers' or 'following'.")

    file_path = select_save_file()
    if not file_path:
        print("No file selected. Exiting.")
        return

    driver = setup_driver()
    try:
        # Open Instagram and wait for login
        open_url(driver, "https://www.instagram.com/")
        print("Please log in to Instagram in the opened browser.")
        while True:
            logged_in = input("Have you already logged in? (yes/no): ").strip().lower()
            if logged_in == "yes":
                break
            elif logged_in == "no":
                print("Please log in and then type 'yes' to continue.")
            else:
                print("Invalid input. Please type 'yes' or 'no'.")

        # Open profile page
        profile_url = f"https://www.instagram.com/{profile_id}/"
        open_url(driver, profile_url)
        print(f"Opened profile: {profile_id}")
        time.sleep(5)

        # Get expected count before clicking the button
        expected_count = get_follower_count(driver)
        if expected_count:
            print(f"Expected number of {list_type}: {expected_count}")

        print(f"Clicking on {list_type} button...")
        click_list_button(driver, list_type)

        print("Identifying account list element...")
        accountlist_div_name = get_accountlist_div_name(driver)
        if not accountlist_div_name:
            print(
                "Could not find the account list element. Please check if the page loaded correctly."
            )
            return

        print(f"Found account list with class name: {accountlist_div_name}")
        print("Starting to scroll and collect usernames. This may take some time...")

        # Number of scrolls before saving to Excel (adjust as needed)
        save_interval = 10

        usernames = incremental_scroll_and_save(
            driver,
            accountlist_div_name,
            file_path,
            expected_count=expected_count,
            scroll_delay=3.0,
            save_interval=save_interval,
        )

        print(f"Process complete! Collected {len(usernames)} unique usernames.")
        print(f"Results saved to: {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
