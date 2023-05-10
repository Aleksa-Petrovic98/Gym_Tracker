import requests
from datetime import datetime
import os

# Define API key, base URL, and app ID
API_KEY = os.environ['API_KEY']
API_BASE_URL = os.environ['API_BASE_URL']
APP_ID = os.environ['APP_ID']

# Define Sheety endpoint
SHEET_ENDPOINT = os.environ['SHEET_ENDPOINT']

# Function to get workout stats using natural language input
def get_workout_stats():
    # Get today's date and current time
    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    # Get user input for exercises
    query = input("Tell me which exercises you did: ")

    # Create API request headers
    headers = {
        'x-app-id': APP_ID,
        'x-app-key': API_KEY,
        'Content-Type': 'application/json',
    }

    # Create API request payload
    payload = {
        'query': query,
        'gender': 'male',
        'weight_kg': 90,
        'height_cm': 187,
        'age': 25
    }

    # Send the API request
    response = requests.post(API_BASE_URL, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the API response
        data = response.json()

        # Extract and print the workout stats for each exercise
        for exercise in data['exercises']:
            sheet_inputs = {
                "workout": {
                    "date": today_date,
                    "time": now_time,
                    "exercise": exercise["name"].title(),
                    "duration": exercise["duration_min"],
                    "calories": exercise["nf_calories"]
                }
            }
            # Send the workout stats to Sheety
            sheet_response = requests.post(SHEET_ENDPOINT, json=sheet_inputs)
            # Print the Sheety response
            print(sheet_response.text)
    else:
        # Print error message if the API request was unsuccessful
        print('Error:', response.status_code)

# Example usage
get_workout_stats()
