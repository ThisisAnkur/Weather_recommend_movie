import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# scraping imdb movies data
def scrape_movies_for_keyword(weather, keyword):

    ''' 1. It collects movies from IMDB based on a given keyword and returns it as a DataFrame.
        2. Arguments:
            - weather: Weather condition used to filter movies.
            - keyword: The keyword used to search for movies.
        3. Returned value:
            - df: A DataFrame of movies collected from IMDB by keyword.
        4. The function searches for movies based on a specific keyword on the IMDB website.
        5. It collects title, genre, rating, description etc. information for each movie.
        6.  Notes:
        - Keyword search is used to search IMDB.
        - Weather parameter can be used to filter movies by weather condition.
    '''
  
    titles = []
    genres = []
    ratings = []
    descriptions = []
    directors = []
    certificates = []
    lead_actor = []
    votess = []
    grosses = []
    years = []

    base_url = "https://www.imdb.com/search/keyword/"
    params = {
        "keywords": keyword,
        "sort": "moviemeter,asc",
        "mode": "detail",
        "title_type": "movie",
    }

    page = 1
    while True:
        params["page"] = page
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        movie_elements = soup.find_all("div", class_="lister-item mode-detail")

        if not movie_elements:
            break

        for movie_element in movie_elements:
            year_element = movie_element.find("span", class_="lister-item-year text-muted unbold")
            year_text = year_element.text if year_element else ""
            years.append(year_text)

            title_element = movie_element.find("h3", class_="lister-item-header")
            title = title_element.a.text.strip() if title_element else "N/A"
            titles.append(title)

            genre_element = movie_element.find("span", class_="genre")
            genre = genre_element.text.strip() if genre_element else "N/A"
            genres.append(genre)

            rating_element = movie_element.find("div", class_="inline-block ratings-imdb-rating")
            rating = rating_element.strong.text.strip() if rating_element else "N/A"
            ratings.append(rating)

            certificate_element = movie_element.find("span", class_ = "certificate")
            certificate = certificate_element.text.strip() if certificate_element else "N/A"
            certificates.append(certificate)
            
            description_element = movie_element.find("p", class_="")
            description = description_element.text.strip() if description_element else "N/A"
            descriptions.append(description)
            
            actor_element = movie_element.select_one("p.ghost a[href^='/name/']")
            actor = actor_element.text if actor_element else "N/A"
            lead_actor.append(actor)

            director_element = movie_element.select_one("p.text-muted.text-small a[href^='/name/']")
            director = director_element.text if director_element else "N/A"
            directors.append(director)

            votes_element = movie_element.find("span", attrs={"name": "nv", "data-value": True})
            votes = votes_element["data-value"] if votes_element else "N/A"
            votess.append(votes)

            gross_element = movie_element.find("span", string="Gross:")
            gross = gross_element.find_next_sibling("span").text.strip() if gross_element else "N/A"
            grosses.append(gross)

        page += 1

    data = {
        "Title": titles,
        "Year": years,
        "Genre": genres,
        "Certificate": certificates,
        "Rating": ratings,
        "Votes": votess,
        "Description": descriptions,
        "Lead": lead_actor,
        "Director": directors,
        "Gross": grosses,
        # "Keyword": keyword,
        "Weather": weather,
    }
    df = pd.DataFrame(data)

    return df


keyword_map = {
    "Rain": ["rain", "rainy-day", "rainy-weather", "melancholy", "coziness", "love-story"],
    "Clear": ["clear-sky", "sun", "sunny", "sunny-day", "sunny-weather", "happiness", "optimism", "inspirational"],
    "Clouds": ["cloud","cloudy-sky", "cloudiness", "daydream", "dream", "contemplation"],
    "Drizzle": ["rainfall", "raindrop", "tranquility", "serenity", "gentleman", "gentlewoman", "peace"],
    "Thunderstorm": ["thunderstorm", "storm", "stormy-weather", "excitement", "hate", "revenge"],
    "Snow": ["snow", "snowing", "winter", "christmas", "wonder", "playfulness", "holiday"],
    "Mist": ["mist", "misty-day", "intrigue", "calmness", "calm", "thriller"],
    "Fog": ["fog", "foggy-night", "uncertainty", "introspection", "psychological-thriller"]
}


movie_dfs = []
for weather, keywords in keyword_map.items():
    for keyword in keywords:
        movie_dfs.append(scrape_movies_for_keyword(weather, keyword))

all_movies_df = pd.concat(movie_dfs, ignore_index=True)

all_movies_df.to_csv('movie_data.csv')