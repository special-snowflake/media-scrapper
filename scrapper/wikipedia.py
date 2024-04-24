from bs4 import BeautifulSoup
import requests
import re
from downloader import download_files

# URL of the page
def wiki(url):
    # Send HTTP request
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.text if soup.title else 'No title found'

        # Remove special characters using regex, retaining alphanumeric and spaces
    clean_title = "wikipedia/" + re.sub(r'[^A-Za-z0-9 ]+', '', title)
    # Find elements by class
    print(clean_title)
    images = []
    for item in soup.select('figure img'):
        if 'srcset' in item.attrs:
            srcset = item['srcset']
            urls = [url.strip().split(' ')[0] for url in srcset.split(',')]
            latest_url = urls[-1]
            images.extend(['https:'+ latest_url])
        else:
            continue
    return images, clean_title

