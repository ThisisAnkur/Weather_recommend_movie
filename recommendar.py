from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


data = pd.read_csv('imdb_movies.csv')

def get_weather(city_name):
    api_key = ' ' # add weathermap api key
    url = 'http://api.openweathermap.org/geo/1.0/direct?'
    response = requests.get(url, params={"q": city_name, "appid": api_key})
    data = response.json()
    
    if data:
        latitude = data[0]["lat"]
        longitude = data[0]["lon"]

        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + f"lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        
        lat_response = requests.get(complete_url)
        weather_data = lat_response.json()
    
        if "weather" in weather_data:
                main_info = weather_data["weather"][0]["main"]
                description = weather_data["weather"][0]["description"]
                temperature = weather_data["main"]["temp"]
                humidity = weather_data["main"]["humidity"]
                pressure = weather_data["main"]["pressure"]
                wind_speed = weather_data["wind"]["speed"]
                

        else:
            print('Weather information not found')
            
    else:
        print('City not Found')
        
    return main_info

def get_movie_poster(api_key, movie_title):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": movie_title
    }

    try:
        response = requests.get(base_url, params=params)
        response_data = response.json()

        if response_data.get("results"):
            movie_results = response_data["results"]
            poster_urls = []

            for movie in movie_results:
                poster_path = movie.get("poster_path")
                if poster_path:
                    poster_urls.append("https://image.tmdb.org/t/p/w500/" + poster_path)
                    break
                else:
                    print(f"Poster path not found for movie '{movie_title}'")

            return poster_urls
            
        else:
            print(f"Movie '{movie_title}' not found.")
            return None

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None 


def get_movies_by_weather(weather_col, tf_idf_col, weather_variable, num_of_recommend):
    dataframe = data
    
    filtered_movies = dataframe[(dataframe[weather_col]==weather_variable)]
    
    num_movies_to_recommend = num_of_recommend
    
    num_movies_available = len(filtered_movies)
    
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(filtered_movies[tf_idf_col])
    
    cosine_sim = cosine_similarity(tfidf_matrix)
    
    random_indices = np.random.choice(num_movies_available, size=num_movies_to_recommend, replace=False)
    
    movie_indices = cosine_sim[0].argsort()
    
    top_movies_indices = movie_indices[random_indices][::-1]

    top_movies = filtered_movies.iloc[top_movies_indices]
    top_movies = top_movies.sort_values("Rating", ascending=False).reset_index()
    del top_movies["index"]

    return top_movies[['Title', 'Year', 'Genre', 'Description', 'Rating', 'Director', 'Votes', 'Weather', 'Season']]
