import os
import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
LEADS_BASE_ID = os.getenv("LEADS_BASE_ID", "appzukRazDqAm3RwI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI
openai = OpenAI(api_key=OPENAI_API_KEY)

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
    
    def get_record(self, record_id: str):
        """Get a specific record from Airtable"""
        url = f"{self.base_url}/{record_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def update(self, record_id: str, fields: dict):
        """Update a record in Airtable"""
        url = f"{self.base_url}/{record_id}"
        payload = {"fields": fields}
        
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()

def generate_demo_brief(lead_data):
    """Generate a demo brief using GPT-4"""
    prompt = f"""
Generate a 200-word demo briefing for Jayashree at Niya to pitch to the following B2B lead:

- Lead Name: {lead_data.get('Lead Name', '')}
- Role: {lead_data.get('Role', '')}
- Company: {lead_data.get('Company Name', '')}
- Industry: {lead_data.get('Industry', '')}
- Company Size: {lead_data.get('Company Size', '')}
- Website/LinkedIn: {lead_data.get('Website/LinkedIn', '')}
- Notes/Objections: {lead_data.get('Notes/Objections', '')}
- Reply Type: {lead_data.get('Reply Type', '')}

The output should include:
1. Summary of what the company likely does
2. What the role's top concern might be
3. A custom angle to pitch Niya's mental fitness bootcamp

Keep it sharp and to the point.
"""
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating brief: {str(e)}"

@app.route('/generate-brief', methods=['GET', 'POST'])
def generate_brief_endpoint():
    """Firebase function endpoint for generating demo briefs"""
    try:
        # Get record ID from query parameters or request body
        if request.method == 'GET':
            record_id = request.args.get('recordId')
        else:
            data = request.get_json()
            record_id = data.get('recordId')
        
        if not record_id:
            return jsonify({
                "success": False,
                "error": "recordId parameter is required"
            }), 400
        
        # Initialize Airtable connection
        airtable = AirtableAPI(LEADS_BASE_ID, "Leads", AIRTABLE_TOKEN)
        
        # Get the lead record
        record = airtable.get_record(record_id)
        lead_data = record['fields']
        
        # Generate the demo brief
        brief = generate_demo_brief(lead_data)
        
        # Update the record with the generated brief
        airtable.update(record_id, {
            "Demo Brief": brief,
            "Brief Generated": True,
            "Brief Generated Date": datetime.now().isoformat()
        })
        
        return jsonify({
            "success": True,
            "recordId": record_id,
            "leadName": lead_data.get('Lead Name', ''),
            "companyName": lead_data.get('Company Name', ''),
            "brief": brief,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "niya-demo-brief-generator"
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with usage instructions"""
    return jsonify({
        "service": "Niya Demo Brief Generator",
        "version": "1.0.0",
        "endpoints": {
            "generate_brief": "/generate-brief?recordId=YOUR_RECORD_ID",
            "health": "/health"
        },
        "usage": "Call /generate-brief with recordId parameter to generate a demo brief for a lead"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 