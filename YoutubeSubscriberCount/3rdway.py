import requests

# YouTube Data API endpoint
url = "https://www.googleapis.com/youtube/v3/channels"

# Parameters
channel_id = "UCeRrIOXI1ASOn_cOchuRkOg"  # Replace with your channel ID
api_key = "AIzaSyAt7Wo80m2M1YU-eNSGB9zF8D9yiUWw7qQ"  # Replace with your API key
params = {
    "part": "statistics",
    "id": channel_id,
    "key": api_key
}

# Send GET request
response = requests.get(url, params=params)

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    subscriber_count = data["items"][0]["statistics"]["subscriberCount"]
    print("Subscriber count:", subscriber_count)
else:
    print("Failed to fetch subscriber count. Status code:", response.status_code)
