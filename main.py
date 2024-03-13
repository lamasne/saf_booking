# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
from functions import *

# Left to do: 1) instead of is_tomorrow use date 2) do the cancel 18:30 trick

max_loading_time = 10  # in seconds
time_of_interest = "17:15"
is_for_tomorrow = False
time_between_attempts = 5  # in seconds
max_number_of_attempts = 1000

# Set up Selenium WebDriver
service = Service(executable_path='./chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to the gym's website and log in
    driver.get("https://uab.deporsite.net/loginmenu")
    username_input = WebDriverWait(
        driver, max_loading_time
    ).until(  # Wait for the element to appear
        EC.presence_of_element_located((By.ID, "email"))
    )
    time.sleep(random_delay())
    username_input.send_keys("Y7645569S")
    password_input = driver.find_element(
        "id", "password"
    )  # Locate the password input field
    time.sleep(random_delay())
    password_input.send_keys("85Isashy85")
    time.sleep(random_delay())
    password_input.send_keys(Keys.RETURN)  # Press Enter to submit the form

    # Navigate to the booking page
    time.sleep(random_delay())
    driver.get(
        "https://uab.deporsite.net/reserva-espais?IdDeporte=531"
    )  # Replace with your gym's website

    # Loop until time of interest becomes available
    nb_of_attempts = 0
    # Go to tommorow's sessions
    if is_for_tomorrow:
        go_to_next_day(driver, max_loading_time)
    availability_found = check_availability(time_of_interest, driver, max_loading_time)
    while not availability_found:
        if nb_of_attempts >= max_number_of_attempts:
            break
        driver.refresh()
        # Go to tommorow's sessions
        if is_for_tomorrow:
            go_to_next_day(driver, max_loading_time)
        availability_found = check_availability(
            time_of_interest, driver, max_loading_time
        )
        nb_of_attempts += 1
        time.sleep(time_between_attempts)

    # Confirm the booking (assuming there's a button to confirm the booking)
    confirm_button = WebDriverWait(
        driver, max_loading_time
    ).until(  # Wait for the element to be present
        EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-modal-horas"))
    )
    time.sleep(random_delay())
    confirm_button[0].click()

    try:
        # Wait for agreement checkbox to be clickable
        agree_terms_check = WebDriverWait(
            driver, max_loading_time
        ).until(  # Wait for the element to be present
            EC.presence_of_element_located((By.ID, "aceptacionCondiciones"))
        )
        # Scroll down to the checkbox
        time.sleep(random_delay())
        driver.execute_script("arguments[0].scrollIntoView();", agree_terms_check)

        # Check the checkbox
        time.sleep(random_delay())
        agree_terms_check.click()

        # Click on continue
        continue_button = WebDriverWait(
            driver, max_loading_time
        ).until(  # Wait for the element to be present
            EC.element_to_be_clickable((By.ID, "btnSiguiente"))
        )
        time.sleep(random_delay())
        continue_button.click()

        # Click on next continue
        reservar_button = WebDriverWait(
            driver, max_loading_time
        ).until(  # Wait for the element to be present
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "div.col-md-3:not(.hidden) .btn-siguiente-pagar:not(.hidden)",
                )
            )
        )

        # reservar_button = WebDriverWait(
        #     driver, max_loading_time
        # ).until(  # Wait for the element to be present
        #     EC.element_to_be_clickable((By.CLASS_NAME, "btn-siguiente-pagar"))
        # )
        time.sleep(random_delay())
        reservar_button[0].click()
        print(f"You have successfully booked for tomorrow/today at {time_of_interest}")
    except Exception as e:
        time.sleep(120)
        print("CANCEL THE BOOKING! You have 2 minutes")

except Exception as e1:
    print("Error:", e1)

# Log out
time.sleep(5)  # Make sure the booking has been processed
driver.get("https://uab.deporsite.net/logout")  # Replace with your gym's website
print("logged out")

# Close the browser
time.sleep(3)  # Make sure I have been logged out
driver.quit()
print("closed the window")
