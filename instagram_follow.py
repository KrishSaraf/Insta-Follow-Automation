from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
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

def random_delay(min_seconds=2, max_seconds=4):
    """Add a random delay between actions to avoid detection."""
    time.sleep(random.uniform(min_seconds, max_seconds))

def handle_popup(driver, wait):
    """Handle various popups that might appear."""
    popups = [
        "//button[contains(text(), 'Not Now')]",
        "//button[text()='Not Now']",
        "//button[contains(text(), 'Maybe Later')]"
    ]
    
    for popup in popups:
        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, popup)))
            button.click()
            random_delay()
            logging.info(f"Handled popup: {popup}")
        except TimeoutException:
            continue

def follow_user(driver, username, wait):
    """Attempt to follow a specific user."""
    profile_url = f"https://www.instagram.com/{username}/"
    driver.get(profile_url)
    
    try:
        # Wait for the profile page to load
        wait.until(EC.presence_of_element_located((By.XPATH, "//header")))
        random_delay()

        # Check if the account exists
        try:
            error_message = driver.find_element(By.XPATH, "//h2[contains(text(), 'Sorry, this page')]")
            if error_message:
                logging.warning(f"Account not found: {username}")
                return False
        except NoSuchElementException:
            pass

        # Try different button selectors
        follow_button_selectors = [
            "//button[contains(., 'Follow')]",
            "//button[text()='Follow']",
            "//div[text()='Follow']/ancestor::button",
            "//div[contains(@class, '_acan')]//button[not(contains(text(), 'Following')) and not(contains(text(), 'Requested'))]"
        ]

        for selector in follow_button_selectors:
            try:
                follow_button = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                
                # Check if already following or requested
                if "Following" in follow_button.text or "Requested" in follow_button.text:
                    logging.info(f"Already following or requested: {username}")
                    return False
                
                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", follow_button)
                random_delay(1, 2)
                
                if follow_button.is_displayed() and follow_button.is_enabled():
                    follow_button.click()
                    logging.info(f"Successfully followed {username}")
                    random_delay(3, 5)  # Longer delay after successful follow
                    return True
            except (TimeoutException, ElementClickInterceptedException):
                continue
            except Exception as e:
                logging.error(f"Error with selector {selector} for {username}: {str(e)}")
                continue

        logging.warning(f"Could not find follow button for {username}")
        return False

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
            random_delay(4, 6)  # Longer delay between users

        logging.info(f"Automation completed. Successfully followed {successful_follows} out of {len(usernames_to_follow)} users.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        if driver:
            driver.quit()
            logging.info("Browser closed.")

if __name__ == "__main__":
    main() 