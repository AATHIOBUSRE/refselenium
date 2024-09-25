import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # WebDriver Manager
import re  # Importing the regular expressions module
#this is checkbranch
# Load the CSV file and read the words
excel_file_path = "csvfile.csv"  
# Set up options for Chrome
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors
chrome_options.add_argument("--start-maximized")  # Start maximized (optional)
# Set up Selenium with WebDriver Manager and options
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
# Open the website
driver.get("https://www.primemoversolutions.in/")

# Wait for the page to load
time.sleep(1)

# Function to escape special characters for regex
def escape_special_characters(word):
    return re.escape(word)

# Function to highlight words in the webpage while preserving case
def highlight_words(words):
    highlight_script = ""
    for word in words:
        # Escape special characters for regex
        escaped_word = escape_special_characters(word)
        # Use a case-insensitive replacement for highlighting
        highlight_script += f"""
        (function() {{
            var bodyText = document.body.innerHTML;
            var searchTerm = '{escaped_word}';
            var regex = new RegExp('(' + searchTerm + ')', 'gi');  // Case-insensitive search
            var highlightedText = '<span style="background-color: yellow; font-weight: bold;">$1</span>';
            document.body.innerHTML = bodyText.replace(regex, highlightedText);
        }})();
        """
    # Execute the JavaScript code to highlight all words
    driver.execute_script(highlight_script)

# Function to remove highlights from the webpage
def remove_highlights():
    remove_script = """
    var bodyText = document.body.innerHTML;
    document.body.innerHTML = bodyText.replace(/<span style="background-color: yellow; font-weight: bold;">(.*?)<\/span>/g, '$1');
    """
    driver.execute_script(remove_script)

# Initialize a set to track previously highlighted words
previous_words = set()

try:
    while True:  # Infinite loop to keep the script running
        # Load the CSV file and get current words
        try:
            df = pd.read_csv(excel_file_path, delimiter=',', quotechar='"', on_bad_lines='skip')  # Adjust the delimiter and quotechar as needed
            current_words = set(df['words'].dropna().tolist())  # Get all valid words
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV: {e}")
            break  # Exit the loop on CSV error

        # Check for changes in the word list
        if current_words != previous_words:
            remove_highlights()  # Remove existing highlights
            highlight_words(current_words)  # Highlight new words
            previous_words = current_words  # Update the set of previous words

        time.sleep(5)  # Wait before checking the CSV file again

except KeyboardInterrupt:
    print("Script stopped manually.")

# Close the browser before exiting
driver.quit()

#this in  a branch1 

