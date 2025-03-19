from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
from functions import *
import config


def book_consec_sessions(users, time_of_interest, is_for_tomorrow):
    '''Books consecutive sessions for all users'''
    session_time = datetime.combine(datetime.now().date(), datetime.strptime(time_of_interest, "%H:%M").time())
    nb_sessions_booked = 0
    while nb_sessions_booked < config.nb_consecutive_sessions_to_book:
        # if nb_sessions_booked > 0:
        wait_for_booking_enabling(session_time)
        book_for_all(users, time_of_interest, is_for_tomorrow)
        nb_sessions_booked += 1
        # Define next session to book
        session_time = session_time + timedelta(minutes=75)
        time_of_interest = "{:02d}".format(session_time.hour) + ":" + "{:02d}".format(session_time.minute)

def book_for_all(users, time_of_interest, is_for_tomorrow):
    '''books session for each user'''
    for user in users:
        if user in config.CREDS.keys():
            username, password = config.CREDS[user]
        else:
            raise ValueError(f"Credentials of user: {user} are unknown")
        book_session(user, username, password, is_for_tomorrow, time_of_interest)

def book_session(user, username, password, is_for_tomorrow, time_of_interest):
    print(f"I will now book a gym session at {time_of_interest} {' tomorrow' if is_for_tomorrow else 'today'} for {user}")

    # driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the gym's website and log in
        driver.get("https://uab.deporsite.net/loginmenu")
        username_input = WebDriverWait(
            driver, config.max_loading_time
        ).until(  # Wait for the element to appear
            EC.presence_of_element_located((By.ID, "email"))
        )
        time.sleep(random_delay())
        username_input.send_keys(username)
        password_input = driver.find_element(
            "id", "password"
        )  # Locate the password input field
        time.sleep(random_delay())
        password_input.send_keys(password)
        time.sleep(random_delay())
        password_input.send_keys(Keys.RETURN)  # Press Enter to submit the form

        # Navigate to the booking page
        time.sleep(random_delay())
        driver.get(
            "https://uab.deporsite.net/reserva-espais?IdDeporte=531"
        ) 

        # Go to tommorow's sessions
        if is_for_tomorrow:
            go_to_next_day(driver, config.max_loading_time)
        
        # Check availability
        availability_found = check_availability(time_of_interest, driver, config.max_loading_time)
        
        # Loop until time of interest becomes available
        nb_of_attempts = 1
        start_time = time.time()
        while not availability_found:
            if nb_of_attempts >= config.max_number_of_attempts:
                raise TimeoutException('Reached the max number of attempts.')
            print(f'Attempt number {nb_of_attempts}')
            driver.refresh()
            # Go to tommorow's sessions
            if is_for_tomorrow:
                go_to_next_day(driver, config.max_loading_time)
            availability_found = check_availability(
                time_of_interest, driver, config.max_loading_time
            )
            nb_of_attempts += 1
            # wait between attempts 
            time.sleep(random_delay(*config.time_between_attempts))  
        end_time = time.time()
        spamming_min, spamming_sec = divmod(end_time - start_time, 60) 
        print(f"Found time availability after {int(spamming_min):} minutes and {int(spamming_sec)} seconds.")

        try:
            # Confirm the booking (assuming there's a button to confirm the booking)
            confirm_button = WebDriverWait(
                driver, config.max_loading_time
            ).until(  # Wait for the element to be present
                EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-modal-horas"))
            )
            time.sleep(random_delay())
            confirm_button[0].click()

            # Wait for agreement checkbox to be clickable
            agree_terms_check = WebDriverWait(
                driver, config.max_loading_time
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
                driver, config.max_loading_time
            ).until(  # Wait for the element to be present
                EC.element_to_be_clickable((By.ID, "btnSiguiente"))
            )
            time.sleep(random_delay())
            continue_button.click()

            # Click on next continue
            reservar_button = WebDriverWait(
                driver, config.max_loading_time
            ).until(  # Wait for the element to be present
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        "div.col-md-3:not(.hidden) .btn-siguiente-pagar:not(.hidden)",
                    )
                )
            )

            # reservar_button = WebDriverWait(
            #     driver, config.max_loading_time
            # ).until(  # Wait for the element to be present
            #     EC.element_to_be_clickable((By.CLASS_NAME, "btn-siguiente-pagar"))
            # )
            time.sleep(random_delay())
            reservar_button[0].click()
            print(f"Congrats! You have successfully booked a gym session at {time_of_interest} {' tomorrow' if is_for_tomorrow else 'today'} for {user}")
        except Exception as e:
            print(e)
            if nb_of_attempts < config.max_number_of_attempts:
                print("Error! I will try again in 2 min")
                time.sleep(120)
                book_session(user, username, password, is_for_tomorrow, time_of_interest)
    except Exception as e1:
        print("Error:", e1)

    # Log out
    time.sleep(5)  # Make sure the booking has been processed
    driver.get("https://uab.deporsite.net/logout")  # Replace with your gym's website
    print("Logged out.")

    # Close the browser
    time.sleep(3)  # Make sure I have been logged out
    driver.quit()
    print("Closed the window.")
