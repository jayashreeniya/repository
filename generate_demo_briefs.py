import os
import requests
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
LEADS_BASE_ID = os.getenv("LEADS_BASE_ID", "appzukRazDqAm3RwI")
TABLE = "Leads"

class AirtableAPI:
    def __init__(self, base_id: str, table_name: str, token: str):
        self.base_id = base_id
        self.table_name = table_name
        self.token = token
        self.base_url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def get_all(self, formula: str = None):
        """Get all records from Airtable"""
        params = {}
        if formula:
            params["filterByFormula"] = formula
        
        response = requests.get(self.base_url, headers=self.headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("records", [])
    
    def update(self, record_id: str, fields: dict):
        """Update a record in Airtable"""
        url = f"{self.base_url}/{record_id}"
        payload = {"fields": fields}
        
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()

at = AirtableAPI(LEADS_BASE_ID, TABLE, AIRTABLE_TOKEN)
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_demos():
    return at.get_all(formula="AND({Demo Booked?}=TRUE, {Demo Brief}='')")

def generate_brief(lead):
    f = lead["fields"]
    prompt = f"""
Generate a 200-word demo briefing for Jayashree at Niya to pitch to the following B2B lead:

- Lead Name: {f.get("Lead Name", "")}
- Role: {f.get("Role", "")}
- Company: {f.get("Company Name", "")}
- Industry: {f.get("Industry", "")}
- Company Size: {f.get("Company Size", "")}
- Website/LinkedIn: {f.get("Website/LinkedIn", "")}
- Notes/Objections: {f.get("Notes/Objections", "")}
- Reply Type: {f.get("Reply Type", "")}

The output should include:
1. Summary of what the company likely does
2. What the role's top concern might be
3. A custom angle to pitch Niya's mental fitness bootcamp

Keep it sharp and to the point.
"""
    res = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content.strip()

def main():
    leads = fetch_demos()
    for lead in leads:
        brief = generate_brief(lead)
        at.update(lead['id'], {"Demo Brief": brief})
        print(f"✅ Brief added for {lead['fields'].get('Lead Name')}")

if __name__ == "__main__":
    main() 