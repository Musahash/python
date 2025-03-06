import requests
from datetime import datetime, timedelta
import schedule
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials
username = "test@707222.xyz"
password = "J%y&~wT(IM3n"
smtp_server = "mail.707222.xyz"
smtp_port = 465  # SSL port


# API Key for OpenWeatherMap
API_KEY = "37ecedf089b57eecffdd7f0dbf58e844"  # Replace this with your OpenWeatherMap API key.


# Function to fetch tomorrow's weather forecast
def get_tomorrow_forecast(location="erbil"):
    try:
        # URL for the 5-day/3-hour forecast API
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&units=metric&appid={API_KEY}'
        result = requests.get(url)

        # Check if the request was successful
        if result.status_code == 200:
            data = result.json()
            current_date = datetime.now()
            tomorrow_date = (current_date + timedelta(days=1)).date()

            # Collect necessary forecast data for tomorrow
            temps_tomorrow = []  # List of temperatures
            weather_descriptions = []  # List of sky/weather conditions
            rain_forecasted = False  # Flag to indicate rain

            for entry in data['list']:
                forecast_time = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
                if forecast_time.date() == tomorrow_date:
                    # Collect temperature
                    temps_tomorrow.append(entry['main']['temp'])

                    # Collect sky/weather descriptions
                    weather_descriptions.append(entry['weather'][0]['description'])

                    # Check for rain
                    if 'rain' in entry or 'Rain' in entry['weather'][0]['main']:
                        rain_forecasted = True

            if temps_tomorrow:
                # Calculate lowest, highest, and average temperature for tomorrow
                lowest_temp = min(temps_tomorrow)
                highest_temp = max(temps_tomorrow)

                # Generate a summary of weather conditions
                unique_weather = ", ".join(set(weather_descriptions))

                # Compose the weather summary
                forecast_summary = (
                    f"Weather forecast for {location} tomorrow:\n"
                    f"🌡 Lowest Temperature: {lowest_temp:.1f}°C\n"
                    f"🌡 Highest Temperature: {highest_temp:.1f}°C\n"
                    f"🌤️ Sky Conditions: {unique_weather}\n"
                )
                if rain_forecasted:
                    forecast_summary += "☔ Rain is expected during the day.\n"
                else:
                    forecast_summary += "🌞 No rain is expected tomorrow.\n"

                return forecast_summary
            else:
                return f"No forecast data available for tomorrow in {location}."
        else:
            return f"Error fetching weather data: {result.status_code} - {result.text}"
    except Exception as e:
        return f"An error occurred while fetching weather: {e}"


# Function to send email
def send_email(subject, content):
    try:
        # Email details
        sender_email = "test@707222.xyz"
        receiver_email = "musabahadin595@gmail.com"  # Replace with the recipient's email

        # Create the email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(content, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")


# Function to fetch forecast and send it via email
def send_weather_forecast_email():
    location = "London"  # Change this to your preferred city
    print("Fetching tomorrow's forecast...")
    forecast = get_tomorrow_forecast(location)
    print("Sending email with the forecast...")
    send_email(subject="Tomorrow's Weather Forecast", content=forecast)

# Schedule the email to be sent every day at a certain time
#schedule.every().day.at("17:37").do(send_weather_forecast_email)  # Adjust the time as needed

#print("Weather forecast automation started!")
#while True:
#    schedule.run_pending()
#    time.sleep(60)  # Wait for 1 minute before checking again
