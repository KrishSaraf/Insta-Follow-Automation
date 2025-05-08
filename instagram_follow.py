from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import random
import logging
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, usernames_to_follow

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_automation.log'),
        logging.StreamHandler()
    ]
)

def setup_driver():
    """Initialize and return the Chrome WebDriver with proper options."""
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-notifications')
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def random_delay():
    """Add a random delay between actions to avoid detection."""
    time.sleep(random.uniform(2, 4))

def handle_popup(driver, wait):
    """Handle various popups that might appear."""
    try:
        # Handle "Save Your Login Info?" popup
        save_info_not_now = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))
        save_info_not_now.click()
        random_delay()
    except TimeoutException:
        logging.info("No 'Save Login Info' popup appeared")

    try:
        # Handle "Turn on Notifications" popup
        notifications_not_now = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))
        notifications_not_now.click()
        random_delay()
    except TimeoutException:
        logging.info("No 'Notifications' popup appeared")

def follow_user(driver, username, wait):
    """Attempt to follow a specific user."""
    profile_url = f"https://www.instagram.com/{username}/"
    driver.get(profile_url)
    
    try:
        # Wait for the profile page to load
        wait.until(EC.presence_of_element_located((By.XPATH, "//header")))
        random_delay()

        # Find follow button
        follow_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Follow') or contains(text(), 'follow')]")
        
        if not follow_elements:
            logging.warning(f"No 'Follow' elements found for {username}")
            return False

        clicked = False
        for elem in follow_elements:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                if elem.is_displayed() and elem.is_enabled():
                    logging.info(f"Found follow button for {username}: {elem.text}")
                    elem.click()
                    logging.info(f"Successfully followed {username}")
                    clicked = True
                    break
            except ElementClickInterceptedException:
                logging.warning(f"Could not click follow button for {username} - element intercepted")
            except Exception as e:
                logging.error(f"Error clicking follow button for {username}: {str(e)}")

        return clicked

    except Exception as e:
        logging.error(f"Error processing {username}: {str(e)}")
        return False

def main():
    driver = None
    try:
        driver = setup_driver()
        wait = WebDriverWait(driver, 10)

        # Login to Instagram
        logging.info("Attempting to log in to Instagram...")
        driver.get('https://www.instagram.com/accounts/login/')
        
        # Enter credentials
        username_input = wait.until(EC.element_to_be_clickable((By.NAME, 'username')))
        username_input.send_keys(INSTAGRAM_USERNAME)
        random_delay()

        password_input = wait.until(EC.element_to_be_clickable((By.NAME, 'password')))
        password_input.send_keys(INSTAGRAM_PASSWORD)
        random_delay()

        # Click login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()
        logging.info("Login successful!")

        # Handle popups
        handle_popup(driver, wait)

        # Process each username
        successful_follows = 0
        for username in usernames_to_follow:
            logging.info(f"Processing user: {username}")
            if follow_user(driver, username, wait):
                successful_follows += 1
            random_delay()

        logging.info(f"Automation completed. Successfully followed {successful_follows} out of {len(usernames_to_follow)} users.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        if driver:
            driver.quit()
            logging.info("Browser closed.")

if __name__ == "__main__":
    main() 