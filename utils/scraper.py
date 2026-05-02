import requests
from bs4 import BeautifulSoup

def scrape_doctors(city, disease):
    query = f"{disease} doctors in {city}"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for g in soup.find_all('div', class_='tF2Cxc')[:5]:
        title = g.find('h3')
        link = g.find('a')

        if title and link:
            results.append({
                "name": title.text,
                "link": link['href']
            })

    return results