from bs4 import BeautifulSoup
import requests
import re

def getdata(url):
    r = requests.get(url)
    r.raise_for_status()  # Raise an exception for HTTP errors
    return r.text

async def get_cards(set_name):
    htmldata = getdata(f"https://mythicspoiler.com/{set_name}")
    soup = BeautifulSoup(htmldata, features='html.parser')
    base_url = f"https://mythicspoiler.com/{set_name}/cards/"
    
    card_urls = []
    for item in soup.find_all('img'):
        src = item['src']
        match = re.match(r'cards/([^"]+\.jpg)', src)
        if match:
            card_name = match.group(1)
            full_url = base_url + card_name
            card_urls.append(full_url)
    return card_urls
