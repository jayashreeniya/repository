import csv
import urllib.parse
import requests
from bs4 import BeautifulSoup

def google_search_linkedin(company, role="People Head"):
    query = f"site:linkedin.com/in {role} {company}"
    url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    for h3 in soup.find_all("h3"):
        a = h3.find_parent("a")
        if a and "linkedin.com/in" in a["href"]:
            return a["href"]
    return ""

def enrich_with_linkedin():
    leads = []
    with open("leads.csv", newline="") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            company = row["Company Name"]
            profile_url = google_search_linkedin(company)
            row["LinkedIn"] = profile_url
            leads.append(row)

    with open("leads_enriched.csv", "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Company Name", "Source URL", "LinkedIn"])
        writer.writeheader()
        writer.writerows(leads)

if __name__ == "__main__":
    enrich_with_linkedin()
