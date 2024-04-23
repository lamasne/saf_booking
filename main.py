from functions import *
from run import run
# from params import CREDS
from dotenv import load_dotenv
import os
import ast
import time
from datetime import datetime, timedelta
import random

users = ['Neil', 'Irfan'] # order counts
# time_of_interest = "17:15"
time_of_interest = "16:00"
is_for_tomorrow = False

CREDS = ast.literal_eval(os.getenv('CREDS'))
max_loading_time = 10  # in seconds
max_number_of_attempts = 1000
time_between_attempts = [2,4]

for user in users:
    if user in CREDS.keys():
        username, password = CREDS[user]
    else:
        raise ValueError(f"Credentials of user: {user} are unknown")
    run(max_loading_time, user, username, password, is_for_tomorrow, time_of_interest, max_number_of_attempts, time_between_attempts)

# Prepare the booking of the next session
booked_session = datetime.combine(datetime.now().date(), datetime.strptime(time_of_interest, "%H:%M").time())
next_session = booked_session + timedelta(minutes=75)
# Wait for the booked session to start to be able to book the next session
delay = round((booked_session - datetime.now()).total_seconds())
if delay > 0:
    print(f"Will now sleep for {timedelta(seconds=delay)} to be able to book the next session: {next_session.time()}")
    time.sleep(delay)

# Perform the actual booking of the next session for each user
time_of_interest_2 = "{:02d}".format(next_session.hour) + ":" + "{:02d}".format(next_session.minute)
for user in users:
    if user in CREDS.keys():
        username, password = CREDS[user]
    else:
        raise ValueError(f"Credentials of user: {user} are unknown")
    run(max_loading_time, user, username, password, is_for_tomorrow, time_of_interest_2, max_number_of_attempts, time_between_attempts)