import os
import requests
import datetime


TODAYS_DATE = str(datetime.datetime.now()).split()
TODAY = TODAYS_DATE[0]
TIME = TODAYS_DATE[1][:5]
NUTRITIONIX_APP_ID = os.environ.get("NUTRITIONIX_APP_ID")
NUTRITIONIX_APP_KEY = os.environ.get("NUTRITIONIX_APP_KEY")
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = "https://api.sheety.co/34bae8c41413bf248912bfb89813a84e/myWorkouts/workouts"
BEARER_TOKEN = os.environ.get("SHEETY_TOKEN")

exercises_done = input("What exercises have you done today? ")

NUTRITIONIX_HEADERS = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_APP_KEY,
    #"Content-Type": "application/json"
}

SHEETY_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": BEARER_TOKEN
}

me = {
    "gender": "male",
    "weight_kg": 136,
    "height_cm": 183,
    "age": 39,
    "query": exercises_done
}

nutritionix_response = requests.post(url=EXERCISE_ENDPOINT, data=me, headers=NUTRITIONIX_HEADERS)
nutritionix_response.raise_for_status()
#response = requests.delete(url="https://api.sheety.co/34bae8c41413bf248912bfb89813a84e/myWorkouts/workouts/2", headers={"Authorization": "Bearer thisismysheetyauthtoken"})
#response.raise_for_status()
#print(response)

try:
    nutritionix_json = nutritionix_response.json()['exercises'][0]
    print(nutritionix_json)
    sheety_json = {
        "workout": {
            "date": TODAY,
            "time": TIME,
            "exercise": nutritionix_json['name'].title(),
            "duration": nutritionix_json['duration_min'],
            "calories": nutritionix_json['nf_calories']
        }
    }
    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_json, headers=SHEETY_HEADERS)
    sheety_response.raise_for_status()
    sheety_json = sheety_response.json()['workout']
    print(sheety_json)
    print(f"Added the following to row {sheety_json['id']}\nDate: {TODAY}\nTime: {TIME}\nType of Exercise: "
          f"{sheety_json['exercise']}\nDuration: {sheety_json['duration']}\nCalories Burned: {sheety_json['calories']}")
except IndexError:
    print("Getting an index error.")

#print(nutritionix_response.content)

