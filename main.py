import os
import datetime
import pandas as pd
import numpy as np
import requests
import json
from decouple import config

current_time = datetime.datetime.now()

api_key = config('API_KEY')
calls = {
    "MostPopularTVs/": "https://imdb-api.com/en/API/MostPopularTVs/",
    "MostPopularMovies/": "https://imdb-api.com/en/API/MostPopularMovies/"
}


def get_api_response():
    """
    This loads a request from the IMDB API, creates directories for the specified calls and saves the data for the day
    """
    for callkey, callvalue in calls.items():
        response = requests.get(callvalue+api_key)

        if os.path.exists(f'{callkey}data-{current_time.day}-{current_time.month}.json') == False:
            os.mkdir(callkey.replace('/', ''))
            with open(f'{callkey}data-{current_time.day}-{current_time.month}.json', mode='w+', encoding='UTF-8') as json_file:
                json.dump(response.json(), json_file, indent=4)
                json_file.close()

        else:
            with open(f'{callkey}data-{current_time.day}-{current_time.month}.json', mode='r', encoding='UTF-8') as json_file:
                topdata = json.load(json_file)
                moviedf = pd.DataFrame.from_dict(topdata['items'])
                json_file.close()
        return moviedf


if __name__ == "__main__":
    get_api_response()
