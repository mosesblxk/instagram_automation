# Instagram Follower/Following Scraper

## Overview

This Python script automates the process of extracting follower and following lists from an Instagram profile using Selenium and BeautifulSoup. It scrolls through the list, extracts usernames, and saves them to an Excel file.

## Features

- Automatically scrolls through the followers/following list until all accounts are loaded
- Extracts followers or following from a specified profile
- Uses Selenium for web interaction and BeautifulSoup for parsing
- Saves extracted usernames to an Excel file

## Requirements

- Python 3.x
- Google Chrome & ChromeDriver
- Selenium
- BeautifulSoup4
- Pandas
- Tkinter (usually comes pre-installed with Python)

You can install the necessary Python packages with the following commands:

```bash
pip install selenium beautifulsoup4 pandas openpyxl
```

## How to Use

1. Clone this repository or download the Python script to your local machine.
2. Ensure you have the necessary dependencies installed as mentioned above.
3. Run the script using Python:

## How to Use

This guide provides a step-by-step walkthrough on using the Instagram Follower/Following Scraper.

**Prerequisites:**

- Ensure you have Python 3.x installed.
- Install the required libraries using pip: `pip install selenium beautifulsoup4 pandas openpyxl`
- Download and install Google Chrome and the corresponding ChromeDriver. Make sure their versions are compatible.

**Steps:**

1.  **Clone the Repository:** Clone this repository to your local machine using `git clone <repository_url>`.

2.  **Run the Script:** Navigate to the project directory and execute the script using: `python instagram_scraper.py`

3.  **Enter Profile ID:** The script will prompt you to enter the Instagram profile ID (username).

4.  **Select List Type:** Choose whether to extract the "followers" or "following" list.

5.  **Log in to Instagram:** A Chrome window will open. Log in to your Instagram account. The script will pause until you confirm you've logged in.

6.  **Select Save Location:** After login, you'll be prompted to choose a location to save the extracted usernames as an Excel file (.xlsx).

**Important Notes:**

- You must manually log in to Instagram.
- Ensure your Chrome and ChromeDriver versions are compatible.
- Instagram's structure might change, potentially requiring script updates.
- Use this script responsibly and ethically. Scraping Instagram data may violate their terms of service. Use at your own risk.



```markdown
# How to Use the Instagram Bio Extractor

This guide provides step-by-step instructions for using the Instagram Bio Extractor script.  This script extracts various information from Instagram profiles, including the bio, website, external links, and more.

**Prerequisites:**

1. **Install Python:** Make sure you have Python 3.x installed on your computer. You can download it from [https://www.python.org/](https://www.python.org/).

2. **Install Required Libraries:** Open your terminal or command prompt and run the following command to install the necessary libraries:

   ```bash
   pip install -r requirements.txt
   ```

   This command assumes you have a `requirements.txt` file in the same directory as the script.  If not, you'll need to install the following libraries individually:

   ```bash
   pip install selenium pandas openpyxl
   ```

3. **Download ChromeDriver:** Download the appropriate ChromeDriver version for your Chrome browser from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).  Make sure the ChromeDriver version matches your Chrome version.  Place the `chromedriver` executable in a location accessible from your system's PATH environment variable (or specify its path in the script).

4. **Prepare an Excel File:** Create an Excel file (.xlsx) with a column named "Usernames".  Enter the Instagram usernames you want to extract information from in this column.  Save the file.


**Steps:**

1. **Run the Script:** Open your terminal or command prompt, navigate to the directory containing `bio_extrator.py`, and run the script using:

   ```bash
   python bio_extrator.py
   ```

2. **Enter File Path:** The script will prompt you to enter the path to your Excel file (the one you created in step 4 of Prerequisites).  Enter the full path to the file.

3. **Log in to Instagram:** A Chrome browser window will open. Log in to your Instagram account. The script will pause until you confirm you've logged in.

4. **Wait for Completion:** The script will process each username, extracting information and saving it to a new Excel file.  The script will save progress periodically and create backup files.

5. **Find Results:** Once the script completes, it will tell you the location of the output file containing the extracted profile information.


**Troubleshooting:**

* **ChromeDriver Issues:** If you encounter errors related to ChromeDriver, double-check that you have downloaded the correct version and that it's in your system's PATH or correctly specified in the script.
* **Selenium Errors:** Selenium errors often indicate problems with the web driver or Instagram's website structure.  Ensure your Chrome browser is up-to-date.
* **Network Issues:**  Ensure you have a stable internet connection.


4. The script will prompt you to enter the Instagram profile ID (the username of the profile you wish to extract data from).
5. Next, you will be asked whether you want to extract the followers or following list. Enter one of the two options: followers or following.
6. The script will open a new Chrome window for you to log in to your Instagram account. You will be prompted to confirm whether you've logged in, and once confirmed, it will proceed with extracting the usernames from the selected list (followers or following).
7. After the usernames are extracted, you will be prompted to select where to save the extracted data as an Excel file. The usernames will be saved in the .xlsx format.

## Notes

- You must manually log in to Instagram via the opened browser.
- Ensure Chrome and ChromeDriver versions match.
- Instagram may change its structure, requiring updates to the script.
- This script is for educational and research purposes only. Scraping Instagram data may violate their terms of service.

Disclaimer

- Use this script responsibly and ensure you comply with Instagram's terms of service when using it. The authors are not responsible for any misuse.
# instagram_automation
