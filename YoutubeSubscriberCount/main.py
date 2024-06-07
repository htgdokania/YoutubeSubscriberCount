import requests
from bs4 import BeautifulSoup
import re
import time

def get_subscriber_count(channel_name, retries=3, delay=5):
    url = f"https://www.youtube.com/c/{channel_name}/about"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for attempt in range(retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all("script")
            print(soup)
            print(soup.find_all("subscriberCountText"))

            # Save script contents to a text file
            with open("scripts_content.txt", "w", encoding="utf-8") as file:
                for script in scripts:
                    if script.string:
                        file.write(script.string + "\n\n")

            for script in scripts:
                script_text = script.string
                if script_text and 'subscriber' in script_text:
                    match = re.search(r'{"content":"([0-9,]+) subscribers"}', script_text)
                    if match:
                        subscriber_count = match.group(1)
                        return subscriber_count
            print("Subscriber count not found in the script tags.")
        else:
            print(f"Failed to retrieve page with status code: {response.status_code}")

        # Wait before retrying
        time.sleep(delay)
        print(f"Retrying... ({attempt + 1}/{retries})")

    return None

if __name__ == "__main__":
    channel_name = "MagicalSAMElectronics"  # YouTube channel name
    subscriber_count = get_subscriber_count(channel_name)
    if subscriber_count:
        print(f"Subscriber Count: {subscriber_count}")
    else:
        print("Failed to retrieve subscriber count.")
