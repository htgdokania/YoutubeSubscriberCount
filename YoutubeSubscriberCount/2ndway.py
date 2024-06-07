import requests
from bs4 import BeautifulSoup
import re

def find_subscriber_count_text(tag):
    return tag.name == "script" and "subscriberCountText" in tag.text


def get_subscriber_count():
    # URL of the YouTube channel page
    url = "https://www.youtube.com/c/MagicalSAMElectronics/about"

    # Send GET request
    response = requests.get(url)

    if response.status_code == 200:
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find script tag containing subscriber count text
        subscriber_count_script = soup.find(find_subscriber_count_text)
        #print(subscriber_count_script.text)
        if subscriber_count_script:
            # Extract subscriber count text
            subscriber_count_text = subscriber_count_script.text

            # Extract subscriber count from text
            start_index = subscriber_count_text.find('"subscriberCountText"')
            end_index = subscriber_count_text.find(' ', start_index)
            subscriber_count_str = subscriber_count_text[start_index:end_index]
            #print(subscriber_count_str)
            number = int(re.search(r'\d+', subscriber_count_str).group())
            return number
        else:
            print("\n\n\nSubscriber count text not found")
            return None
    else:
        print(f"Error getting HTTP response code: {response.status_code}")
        return None


if __name__ == "__main__":
    subscriber_count = get_subscriber_count()
    if subscriber_count is not None:
        print("Subscriber Count:", subscriber_count)
