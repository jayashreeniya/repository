import csv
import os
from airtable import Airtable
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = "Leads"

def upload_to_airtable():
    airtable = Airtable(BASE_ID, TABLE_NAME, AIRTABLE_API_KEY)
    with open("leads_enriched.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            airtable.insert({
                "Company Name": row["Company Name"],
                "Source URL": row["Source URL"],
                "LinkedIn": row["LinkedIn"]
            })

if __name__ == "__main__":
    upload_to_airtable()
