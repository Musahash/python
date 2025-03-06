import requests
from datetime import datetime, timedelta

# Secure way to input an API key
api_key = "37ecedf089b57eecffdd7f0dbf58e844"  # Replace with your OpenWeather API key

while True:
    # Input the location
    location = input('Enter the location (or type 0 to quit): ')

    # If the user enters 0, exit the program
    if location == '0':
        print("Exiting the program. Goodbye!")
        break

    try:
        # Fetch current weather
        current_weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}')
        current_weather_response.raise_for_status()  # Raise an error for non-200 HTTP responses

        # Fetch 5-day weather forecast
        forecast_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?q={location}&units=metric&appid={api_key}')
        forecast_response.raise_for_status()  # Raise an error for non-200 HTTP responses
    except requests.exceptions.HTTPError as http_err:
        if current_weather_response.status_code == 404:  # City not found
            print(f"No city found for '{location}'. Please try again with a valid city name.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
    else:
        # Parse current weather data
        current_weather_data = current_weather_response.json()
        current_temp = current_weather_data['main']['temp']
        temp_min = current_weather_data['main']['temp_min']
        temp_max = current_weather_data['main']['temp_max']

        # Display current weather
        print(f"\nWeather in {location} now: {current_weather_data['weather'][0]['description']}")
        print(f"Current Temperature: {current_temp}°C")
        print(f"Highest Temperature: {temp_max}°C")
        print(f"Lowest Temperature: {temp_min}°C")

        # Parse forecast data
        forecast_data = forecast_response.json()
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_date = tomorrow.date()

        # Extract tomorrow's temperature and rain/snow data
        tomorrow_temps = []
        rain_forecasted = False  # Track if rain is forecasted
        snow_forecasted = False  # Track if snow is forecasted

        for forecast in forecast_data['list']:
            forecast_time = datetime.fromtimestamp(forecast['dt'])
            if forecast_time.date() == tomorrow_date:  # Check if forecast date matches tomorrow
                tomorrow_temps.append(forecast['main']['temp'])

                # Check for rain in the forecast
                if 'rain' in forecast and forecast['rain'].get('3h', 0) > 0:
                    rain_forecasted = True
                elif 'Rain' in [w['main'] for w in forecast['weather']]:
                    rain_forecasted = True

                # Check for snow in the forecast
                if 'snow' in forecast and forecast['snow'].get('3h', 0) > 0:
                    snow_forecasted = True
                elif 'Snow' in [w['main'] for w in forecast['weather']]:
                    snow_forecasted = True

        if tomorrow_temps:
            # Calculate min and max temperature for tomorrow
            temp_min_tomorrow = min(tomorrow_temps)
            temp_max_tomorrow = max(tomorrow_temps)

            print(f"\nTomorrow's Weather in {location}:")
            print(
                f"Highest Temperature: {temp_max_tomorrow}°C 🌞" if temp_max_tomorrow > 30 else f"Highest Temperature: {temp_max_tomorrow}°C")
            print(
                f"Lowest Temperature: {temp_min_tomorrow}°C ❄️" if temp_min_tomorrow < 0 else f"Lowest Temperature: {temp_min_tomorrow}°C")

            # Display whether it's likely to rain or snow
            if snow_forecasted:
                print("Snow is expected tomorrow ❄️.")
            elif rain_forecasted:
                print("It is likely to rain tomorrow ☔.")
            else:
                print("No snow or rain is expected tomorrow.")
        else:
            print("\nNo data available for tomorrow's weather.")
        print()  # Blank line for better readability
