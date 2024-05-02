import os
import ast

# Parameters
CREDS = ast.literal_eval(os.getenv('CREDS'))
max_loading_time = 10  # in seconds
max_number_of_attempts = 1000
time_between_attempts = [2,4] # window in seconds
nb_consecutive_sessions_to_book = 3