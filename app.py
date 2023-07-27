import requests
import streamlit as st
import pandas as pd
from PIL.Image import Image
from recommendar import get_weather, get_movies_by_weather, get_movie_poster

weather_img = {
                "Clear": "https://images.pexels.com/photos/1647177/pexels-photo-1647177.jpeg",
                "Clouds": "https://images.pexels.com/photos/531756/pexels-photo-531756.jpeg",
                "Rain":  "https://images.pexels.com/photos/1529360/pexels-photo-1529360.jpeg",
                "Drizzle": "https://images.pexels.com/photos/7002970/pexels-photo-7002970.jpeg",
                "Thunderstorm": "https://images.pexels.com/photos/1118869/pexels-photo-1118869.jpeg",
                "Snow": "https://images.pexels.com/photos/1710352/pexels-photo-1710352.jpeg",
                "Mist": "https://images.pexels.com/photos/691668/pexels-photo-691668.jpeg",
                "Fog": "https://images.pexels.com/photos/1287075/pexels-photo-1287075.jpeg", 
                }

weather_colors = {
    "Clear": "#E6F4F1",
    "Clouds": "#FFFFFF",
    "Rain": "#D8E6ED",
    "Drizzle": "#FAF8FF",  
    "Thunderstorm": "#FEFAE6",  
    "Snow": "#F3FAFF",  
    "Mist": "#FAF7FF",  
    "Fog": "#F4F9FF",  
}

def footer(background_color=""):
    st.markdown(
        f"""
        <style>
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            padding: 10px;
            text-align: center;
            background-color: {background_color};
        }}
        
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 10px;
        }}
        .grid-item {{
            text-align: center;
        }}
        .name {{
            color: aquamania;
            font-weight: bold;
            margin-bottom: 5px;
            text-shadow: black 0.1em 0.1em 0.1em;
        }}
        .links {{
            display: flex;
            justify-content: center;
            margin-top: 5px;
        }}
        .links a {{
            color: white;
            margin: 0 5px;
        }}
        .links a:visited {{color: #d3f2ef}} 
        .links a:hover {{color: #bcaedf}}
        </style>
        """,
        unsafe_allow_html=True
    )



def body_style():
    st.markdown(
        f"""
        <style>
        #MainMenu, header, footer {{
            visibility: hidden;
        }}
        body {{
            background-color: #d3f2ef;
            font-family: 'Source Sans Pro', sans-serif !important;
        }}
        h1 {{
            color: mediumaquamarine;
            text-shadow: black 0.2em 0.2em 0.2em;
        }}
        label {{
            color: white;
            text-shadow: black 0.2em 0.2em 0.2em;
        }}

        img {{
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }}

        .css-ffhzg2 {{
            background: rgb(37,29,57);
            background: -moz-radial-gradient(circle, rgba(37,29,57,1) 0%, rgba(44,45,69,1) 29%, rgba(57,74,90,1) 65%, rgba(76,118,123,1) 95%, rgba(76,118,123,1) 100%, rgba(96,165,158,1) 100%);
            background: -webkit-radial-gradient(circle, rgba(37,29,57,1) 0%, rgba(44,45,69,1) 29%, rgba(57,74,90,1) 65%, rgba(76,118,123,1) 95%, rgba(76,118,123,1) 100%, rgba(96,165,158,1) 100%);
            background: radial-gradient(circle, rgba(37,29,57,1) 0%, rgba(44,45,69,1) 29%, rgba(57,74,90,1) 65%, rgba(76,118,123,1) 95%, rgba(76,118,123,1) 100%, rgba(96,165,158,1) 100%);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#251d39",endColorstr="#60a59e",GradientType=1);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():

    body_style()
    st.title("Movie According Weather of City")
    st.subheader("Discover the perfect movies according weather of your city!")
    city = st.text_input("Enter your city name:")
    if st.button("Get Recommendations"):
        if city:
            try:
                weather = get_weather(city)
                if weather:
                    background_image = weather_img.get(weather)
                    weather_color = weather_colors.get(weather)
                    if background_image:
                        st.markdown(
                            f"""
                            <style>
                            h3 {{
                                color: white;
                                text-shadow: black 0.2em 0.2em 0.2em;
                            }}
                        
                            [data-testid="stAppViewContainer"]{{
                            background: url('{background_image}');
                                background-size: cover;
                            }}
                        
                            div.css-ocqkz7.e1tzin5v3 {{
                                background-color: {weather_color};
                                border: 2px solid #CCCCCC;
                                padding: 5% 5% 5% 10%;
                                border-radius: 5px;
                                color: black;
                                text-align: center;
                                display: flex;
                                box-shadow: 0 3px 10px rgb(0 0 0 / 0.2);
                            }}

                            div.css-ocqkz7.e1tzin5v4{{
                            background-color: white;
                            width: 750px;
                            height: 700px;
                            padding: 5%

                            }}
                            
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
            except Exception as e:
                st.warning("You have given wrong city name: Please check City name!")
                return

            st.subheader(f"{weather} in {city} city")
            container = st.container()
            with container:
                st.subheader(f"Movie recommend")
                recommended_movies = get_movies_by_weather("Weather", "Description", weather, 3)

                api_key = " "  # add tmdb api key
                
                movie_titles = recommended_movies['Title'].tolist()

                poster_urls = []

                for title in movie_titles:
                    poster_url = get_movie_poster(api_key, title)
                    poster_urls.append(poster_url)

                recommended_movies['Poster_url'] = poster_urls
   
            col1, col2, col3 = st.columns(3)
           
            with col1:
                st.image(recommended_movies.loc[0, "Poster_url"], width=200)
                st.write(recommended_movies.loc[0, "Title"])
                st.write(recommended_movies.loc[0, "Genre"])
                st.write(recommended_movies.loc[0, "Rating"])
                st.write(recommended_movies.loc[0, "Description"])

            with col2:
                st.image(recommended_movies.loc[1, "Poster_url"], width=200)
                st.write(recommended_movies.loc[1, "Title"])
                st.write(recommended_movies.loc[1, "Genre"])
                st.write(recommended_movies.loc[1, "Rating"])
                st.write(recommended_movies.loc[1, "Description"])

            with col3:
                st.image(recommended_movies.loc[2, "Poster_url"], width=200)
                st.write(recommended_movies.loc[2, "Title"])
                st.write(recommended_movies.loc[2, "Genre"])
                st.write(recommended_movies.loc[2, "Rating"])
                st.write(recommended_movies.loc[2, "Description"])

        
    
        


if __name__ == "__main__":
    main()
