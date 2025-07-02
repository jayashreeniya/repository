from flask import Flask, request, jsonify
import openai
import os
from airtable import Airtable
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE = "Leads"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

at = Airtable(BASE_ID, TABLE, AIRTABLE_API_KEY)

@app.route("/generate-brief", methods=["GET"])
def generate_brief():
    record_id = request.args.get("recordId")
    record = at.get(record_id)
    f = record['fields']

    prompt = f"""
Generate a 200-word demo briefing for Jayashree at Niya to pitch to the following B2B lead:

- Lead Name: {f.get('Lead Name', '')}
- Role: {f.get('Role', '')}
- Company: {f.get('Company Name', '')}
- Industry: {f.get('Industry', '')}
- Company Size: {f.get('Company Size', '')}
- Website/LinkedIn: {f.get('Website/LinkedIn', '')}
- Notes/Objections: {f.get('Notes/Objections', '')}
- Reply Type: {f.get('Reply Type', '')}

Output: Company summary, likely concerns, and pitch angle for Niya.
"""
    res = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    brief = res.choices[0].message.content.strip()
    at.update(record_id, {"Demo Brief": brief})
    return jsonify({"status": "success", "brief": brief})

# Firebase function entry point
def firebase_function(request):
    return app(request)
