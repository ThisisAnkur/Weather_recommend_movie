# Weather_recommend_movie
Movie  Recommendations by Weather

# Purpose of The Project
Recommend movies according to instant weather information.

A study was conducted by extracting data from eight different weather sources via the Open Weather API and by utilizing keywords from the IMDB datasets.
This study aimed to match the weather information with seasonal patterns found in the IMDB dataset,  resulting in movie recommendations.

# Project Steps
Open Weather API
8 different weather information that the user is expected to enter has been determined from the address https://openweathermap.org/api. 
We kept this weather information in the weather variable.

"Clear": The weather is clear and sunny.
"Clouds": It's cloudy.
"Rain": It's raining.
"Drizzle" (Drizzle): Light raindrops are falling.
"Thunderstorm": There is heavy rain, lightning and thunder.
"Snow" (Snow): It is snowing.
"Mist" (Foggy): Foggy weather conditions.
"Fog" (Dense Fog): Weather conditions with heavy fog.

# Web Scraping
IMDB
We can search for keywords on IMDB's website. The "Keywords" feature is a feature that allows movies or other content to be associated with specific topics in the IMDb 
database. Keywords entered in this section refer to information about the content, theme, subject or other features of the movies.

For example, when you enter a keyword like "rainy weather" or "rainy day", IMDb will associate the relevant movies with the rainy weather or rainy day themes.
This ensures that search results are limited to movies related to these themes. Keywords are used to describe the movie or refer to a particular subject or atmosphere.

We searched for keywords based on 8 weather conditions we pulled from the Open Weather API.
For example, in addition to keywords such as rainy weather for Rain, we also considered words such as melancholy that occurs in people in a rainy weather atmosphere 
and pulled the data through the BeautifulSoup library.

# Recommendations
First, we match/match the weather variable we receive from the user with the movie contents that contain the weather information in our own dataset.
Then, using a hybrid approach, we calculate the frequency of words using the TF-IDF method, and recommend a movie in decreasing order according to the rating of the
movie.

# Movie Posters
tmdb
we also add  poster feature, firstly fetch poster from the tmdb website through api key, we recieve recommeded movies after this fetching the movie poster
based on recommended movie titles.

# Streamlit
We decided to present it to users with an interface using Streamlit. In the recommender.py we created, we called functions that predict movies and in Streamlit and 
used them for each weather condition. We wanted to change the background image specific to each weather condition. We published the site we created on Streamlit.
