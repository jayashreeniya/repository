import requests
from bs4 import BeautifulSoup
import csv

def scrape_inc42_startups():
    url = "https://inc42.com/startups/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Placeholder parsing logic (modify for real HTML structure)
    companies = []
    for article in soup.find_all("article"):
        name = article.find("h2")
        link = article.find("a")["href"]
        if name:
            companies.append({
                "Company Name": name.get_text(strip=True),
                "Source URL": link
            })

    with open("leads.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Company Name", "Source URL"])
        writer.writeheader()
        writer.writerows(companies)

if __name__ == "__main__":
    scrape_inc42_startups()
