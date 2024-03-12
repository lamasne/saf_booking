from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
from functions import *

max_loading_time = 10 # in seconds
time_of_interest = "17:15"
is_for_tomorrow = True
time_between_attempts = 5 # in seconds

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Or choose the appropriate WebDriver for your browser

try:
    # Navigate to the gym's website and log in
    driver.get("https://uab.deporsite.net/loginmenu")
    username_input = WebDriverWait(driver, max_loading_time).until( # Wait for the element to appear
        EC.presence_of_element_located((By.ID, "email"))
    )
    time.sleep(random_delay())
    username_input.send_keys("Y7645569S")
    password_input = driver.find_element("id", "password")  # Locate the password input field
    time.sleep(random_delay())
    password_input.send_keys("85Isashy85")
    time.sleep(random_delay())
    password_input.send_keys(Keys.RETURN)  # Press Enter to submit the form

    # Navigate to the booking page
    time.sleep(random_delay())
    driver.get("https://uab.deporsite.net/reserva-espais?IdDeporte=531")  # Replace with your gym's website

    # Go to tommorow's sessions
    if is_for_tomorrow:
        next_day_button_ls = WebDriverWait(driver, max_loading_time).until( # Wait for the element to be present
            EC.presence_of_all_elements_located((By.CLASS_NAME, "next-day"))
        )    
        time.sleep(random_delay())
        next_day_button_ls[0].click()

    # Loop until time of interest becomes available
    availability_found = check_availability(time_of_interest, driver, max_loading_time)
    while not availability_found:
        driver.refresh()
        time.sleep(time_between_attempts)
        availability_found = check_availability(time_of_interest, driver, max_loading_time)

    # Confirm the booking (assuming there's a button to confirm the booking)
    confirm_button = WebDriverWait(driver, max_loading_time).until( # Wait for the element to be present
        EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-modal-horas"))
    )            
    time.sleep(random_delay())
    confirm_button[0].click()

    # Wait for agreement checkbox to be clickable 
    agree_terms_check = WebDriverWait(driver, max_loading_time).until( # Wait for the element to be present
        EC.presence_of_element_located((By.ID, "checkAceptacionCondiciones"))
    )
    # Scroll down to the checkbox
    time.sleep(random_delay())
    driver.execute_script("arguments[0].scrollIntoView();", agree_terms_check)

    # Ensure the checkbox is visible and enabled
    if agree_terms_check.is_displayed() and agree_terms_check.is_enabled():
        # Check the checkbox
        time.sleep(random_delay())
        agree_terms_check.click()
    else:
        raise WebDriverException("Checkbox is not visible or enabled")

    # Click on continue
    continue_button = WebDriverWait(driver, max_loading_time).until( # Wait for the element to be present
        EC.element_to_be_clickable((By.ID, "btnSiguiente"))
    )    
    time.sleep(random_delay())
    continue_button.click()

except Exception as e:
    print('Error:', e)

# Log out
time.sleep(random_delay())
driver.get("https://uab.deporsite.net/logout")  # Replace with your gym's website
time.sleep(3)  
print('logged out')

# Close the browser
driver.quit()
print('closed the window')
