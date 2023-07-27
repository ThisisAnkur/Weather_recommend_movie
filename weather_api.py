import requests

# weathe Data through Api
def get_weather(city_name):
    api_key = ' '  # Add  OpenWeatherMap API key here
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
                
                print("*******Weather Report*******")
                print(f"City: {city_name}")
                print(f"Today's weather: {main_info}")
                print(f"Description: {description}")
                print(f"Heat: {temperature} °C")
                print(f"Humidity: {humidity}%")
                print(f"Wind: {wind_speed} m/s")
                
        else:
            print('Weather information not found')
            
    else:
        print('City not Found')
        
    return main_info

city_name = input("Enter City Name: ")

weather = get_weather(city_name)

weather 