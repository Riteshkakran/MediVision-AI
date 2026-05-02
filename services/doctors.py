# import requests
# from bs4 import BeautifulSoup

# def get_doctors_service(city, disease):
#     query = f"{disease} doctors in {city}"
#     search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }

#     results = []

#     try:
#         response = requests.get(search_url, headers=headers, timeout=5)
#         soup = BeautifulSoup(response.text, "html.parser")

#         for g in soup.find_all('div', class_='tF2Cxc')[:5]:
#             title = g.find('h3')
#             link = g.find('a')

#             if title and link:
#                 results.append({
#                     "name": title.text,
#                     "link": link['href']
#                 })

#     except Exception as e:
#         print("Scraping failed:", e)

#     # Fallback safety
#     if not results:
#         results = [{
#             "name": "View doctors on Google",
#             "link": search_url
#         }]

#     return {
#         "query": query,
#         "search_link": search_url,
#         "results": results
#     }

import requests
from bs4 import BeautifulSoup

def get_doctors_service(city, disease):
    query = f"{disease} doctors in {city}"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    headers = {"User-Agent": "Mozilla/5.0"}

    results = []

    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        for g in soup.find_all('div', class_='tF2Cxc')[:5]:
            title = g.find('h3')

            if title:
                results.append({
                    "name": title.text
                })

    except Exception as e:
        print("Error:", e)

    return results