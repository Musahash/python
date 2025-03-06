import requests

# Open the file containing the API key and read it
api_key = open('api_key.txt', 'r').read().strip()  # Use 'r' for reading the file

# Input the location
location = input('Location: ')

# Make the API request
result = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}')

# Print the result
if result.status_code == 200:
    data = result.json()
    print(f"Weather in {location}: {data['weather'][0]['description']}")
    print(f"Temperature: {data['main']['temp']}°C")
else:
    print(f"Error: {result.status_code}, {result.text}")
