import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def random_delay():
    """
    Generates a random delay between 1 and 3 seconds to mimic human behavior.
    """
    return random.uniform(1, 2)


def check_availability(time_string, driver, max_loading_time):
    time.sleep(3)  # Gives time for the right schedule to show
    # Find the available sessions for today
    available_sessions = WebDriverWait(
        driver, max_loading_time
    ).until(  # Wait for the element to be present
        EC.presence_of_all_elements_located((By.CLASS_NAME, "hora-sininfo"))
    )
    for session in available_sessions:
        if time_string in session.text:  # Check if the session is at 17:15
            time.sleep(0.2)
            try:
                session.click()  # Click on the session
                print("Time is available")
                return True
            except Exception as e:
                print("Time is currently not available")
                return False


def go_to_next_day(driver, max_loading_time):
    next_day_button_ls = WebDriverWait(
        driver, max_loading_time
    ).until(  # Wait for the element to be present
        EC.presence_of_all_elements_located((By.CLASS_NAME, "next-day"))
    )
    time.sleep(random_delay())
    next_day_button_ls[0].click()
