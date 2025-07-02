import os, time, base64
import re
import requests
import urllib.parse
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from googleapiclient.discovery import build
from google.oauth2 import service_account
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
LEADS_BASE_ID = os.getenv("LEADS_BASE_ID", "appzukRazDqAm3RwI")
KPIS_BASE_ID = os.getenv("KPIS_BASE_ID", "app5MfJmA49we1vjM")
LEADS_TABLE = "Imported table"
KPIS_TABLE = "Imported table"
CALENDLY_LINK = os.getenv("CALENDLY_LINK", "https://calendly.com/niya/15min")
EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "gmail").lower()
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Initialize services
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Airtable with Personal Access Token

class AirtableAPI:
    def __init__(self, base_id: str, table_name: str, token: str):
        self.base_id = base_id
        self.table_name = table_name
        self.token = token
        # URL encode the table name to handle spaces
        import urllib.parse
        encoded_table_name = urllib.parse.quote(table_name)
        self.base_url = f"https://api.airtable.com/v0/{base_id}/{encoded_table_name}"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def get_all(self, formula: str = None) -> List[Dict]:
        """Get all records from Airtable"""
        params = {}
        if formula:
            params["filterByFormula"] = formula
        
        response = requests.get(self.base_url, headers=self.headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("records", [])
    
    def update(self, record_id: str, fields: Dict) -> Dict:
        """Update a record in Airtable"""
        url = f"{self.base_url}/{record_id}"
        payload = {"fields": fields}
        
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def create(self, fields: Dict) -> Dict:
        """Create a new record in Airtable"""
        payload = {"fields": fields}
        
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()

# Initialize Airtable connections
leads_at = AirtableAPI(LEADS_BASE_ID, LEADS_TABLE, AIRTABLE_TOKEN)
kpis_at = AirtableAPI(KPIS_BASE_ID, KPIS_TABLE, AIRTABLE_TOKEN)

class NiyaSalesAgent:
    def __init__(self):
        self.kpis = {
            "emails_sent": 0,
            "replies_received": 0,
            "positive_replies": 0,
            "meetings_booked": 0,
            "calendly_clicks": 0
        }
    
    def fetch_leads(self, status_filter: str = "new") -> List[Dict]:
        """Fetch leads based on status filter"""
        if status_filter == "new":
            formula = "AND({Email Sent?}='FALSE', {Email}!='')"
        elif status_filter == "follow_up":
            formula = "AND({Email Sent?}='TRUE', {Last Email Sent}!='', {Reply Type}='')"
        elif status_filter == "positive":
            formula = "{Reply Type}='Interested'"
        else:
            formula = ""
        
        return leads_at.get_all(formula=formula) if formula else leads_at.get_all()
    
    def generate_cold_email(self, fields: Dict) -> str:
        """Generate personalized cold email using GPT-4"""
        prompt = f"""
        Write a compelling 3-4 line personalized outbound email from Niya to {fields.get('Lead Name', 'the prospect')} 
        who is a {fields.get('Role', 'decision maker')} at {fields.get('Company Name', 'their company')}.
        
        Company context: {fields.get('Company Description', '')}
        Stage: {fields.get('Stage', 'Series B/C')}
        
        The email should:
        1. Be personalized and relevant to their role/company
        2. Mention their company stage if relevant
        3. Offer a 15-minute discovery call
        4. Include a Calendly link: {CALENDLY_LINK}
        5. Be professional but conversational
        6. End with a clear call-to-action
        
        Format: Subject line on first line, then email body.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    
    def generate_follow_up_email(self, fields: Dict, attempt: int = 1) -> str:
        """Generate follow-up email based on attempt number"""
        follow_up_prompts = {
            1: "Send a friendly 3-day follow-up asking if they had a chance to review the initial email",
            2: "Send a 7-day follow-up with additional value proposition or case study",
            3: "Send a final 14-day follow-up with a different angle or offer"
        }
        
        prompt = f"""
        Write a {follow_up_prompts.get(attempt, 'follow-up')} email to {fields.get('Lead Name', 'the prospect')} 
        at {fields.get('Company Name', 'their company')}.
        
        Previous context: {fields.get('Notes/Objections', '')}
        Original email sent: {fields.get('Last Email Sent', '')}
        
        Include the Calendly link: {CALENDLY_LINK}
        Keep it professional and respectful.
        """
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.6
        )
        return response.choices[0].message.content.strip()
    
    def classify_reply(self, reply_text: str) -> Dict:
        """Classify email reply using GPT-4"""
        prompt = f"""
        Analyze this email reply and classify it into one of these categories:
        - Interested: Wants to learn more, asks questions, shows genuine interest
        - Later: Not ready now but might be interested later, asks to follow up
        - Not Now: Not interested, objections, declines
        - Wrong Person: Not the right contact, should be someone else
        - Meeting Booked: Confirms meeting or calendar booking via Calendly
        
        Reply: {reply_text}
        
        Return JSON format:
        {{
            "category": "Interested/Later/Not Now/Wrong Person/Meeting Booked",
            "confidence": 0.95,
            "key_points": ["point1", "point2"],
            "next_action": "suggested next step",
            "calendly_clicked": true/false
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3
        )
        
        try:
            import json
            return json.loads(response.choices[0].message.content.strip())
        except:
            return {
                "category": "Neutral",
                "confidence": 0.5,
                "key_points": ["Unable to parse classification"],
                "next_action": "Manual review needed"
            }
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email via Gmail API or SMTP (Zoho)"""
        if EMAIL_PROVIDER == "gmail":
            try:
                msg = f"To: {to}\r\nSubject: {subject}\r\n\r\n{body}"
                import base64
                from email.mime.text import MIMEText
                message = MIMEText(body)
                message["to"] = to
                message["subject"] = subject
                raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
                message_body = {"raw": raw}
                GMAIL.users().messages().send(userId="me", body=message_body).execute()
                return True
            except Exception as e:
                print(f"❌ Gmail send failed: {e}")
                return False
        else:
            # SMTP (Zoho or other)
            try:
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart
                msg = MIMEMultipart()
                msg["From"] = SMTP_USERNAME
                msg["To"] = to
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))
                with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                    server.login(SMTP_USERNAME, SMTP_PASSWORD)
                    server.sendmail(SMTP_USERNAME, to, msg.as_string())
                return True
            except Exception as e:
                print(f"❌ SMTP send failed: {e}")
                return False
    
    def check_calendly_clicks(self, email: str) -> bool:
        """Check if Calendly link was clicked (simplified version)"""
        # In a real implementation, you'd integrate with Calendly webhooks
        # For now, we'll simulate this based on reply content
        return "calendly" in email.lower() or "book" in email.lower()
    
    def update_lead_status(self, record_id: str, updates: Dict):
        """Update lead status in Airtable"""
        try:
            leads_at.update(record_id, updates)
        except Exception as e:
            print(f"Error updating record {record_id}: {e}")
    
    def log_kpis(self, kpis: Dict):
        """Log KPIs to the KPIs base"""
        try:
            week_start = datetime.now().date() - timedelta(days=datetime.now().weekday())
            kpi_record = {
                "Week Start": week_start.isoformat(),
                "Total Leads": kpis["total_leads"],
                "Emails Sent": kpis["emails_sent"],
                "Interested Replies": kpis["reply_breakdown"]["interested"],
                "Later Replies": kpis["reply_breakdown"]["later"],
                "Not Now Replies": kpis["reply_breakdown"]["not_now"],
                "Wrong Person Replies": kpis["reply_breakdown"]["wrong_person"],
                "Meetings Booked": kpis["reply_breakdown"]["meeting_booked"],
                "Calendly Clicks": kpis["calendly_metrics"]["clicks"],
                "Demos Booked": kpis["calendly_metrics"]["demos_booked"],
                "Reply Rate": round(kpis["overall_rates"]["reply_rate"], 2),
                "Meeting Rate": round(kpis["overall_rates"]["meeting_rate"], 2),
                "Demo Rate": round(kpis["overall_rates"]["demo_rate"], 2),
                "Total Follow-up Attempts": kpis["follow_up_metrics"]["total_attempts"]
            }
            
            # Check if week already exists
            existing_records = kpis_at.get_all(f"{{Week Start}}='{week_start.isoformat()}'")
            if existing_records:
                # Update existing record
                kpis_at.update(existing_records[0]["id"], kpi_record)
                print(f"📊 Updated KPIs for week starting {week_start.isoformat()}")
            else:
                # Create new record
                kpis_at.create(kpi_record)
                print(f"📊 Logged KPIs for week starting {week_start.isoformat()}")
                
        except Exception as e:
            print(f"Error logging KPIs: {e}")
    
    def process_new_leads(self):
        """Process new leads that haven't been emailed yet"""
        print("🔄 Processing new leads...")
        leads = self.fetch_leads("new")
        
        for record in leads:
            fields = record['fields']
            print(f"📧 Sending email to {fields.get('Lead Name', 'Unknown')} at {fields.get('Company Name', 'Unknown')}")
            
            # Generate and send email
            email_content = self.generate_cold_email(fields)
            lines = email_content.split('\n')
            subject = lines[0]
            body = '\n'.join(lines[1:])
            
            if self.send_email(fields['Email'], subject, body):
                self.kpis["emails_sent"] += 1
                
                # Update Airtable
                self.update_lead_status(record['id'], {
                    "Email Sent?": True,
                    "Last Email Sent": datetime.now().date().isoformat(),
                    "AI Suggested Next Step": "Awaiting reply; follow up in 3 days",
                    "Follow-up Attempts": 0
                })
                
                print(f"✅ Email sent successfully to {fields.get('Email', 'Unknown')}")
                time.sleep(2)  # Rate limiting
    
    def process_follow_ups(self):
        """Process leads that need follow-up emails"""
        print("🔄 Processing follow-ups...")
        leads = self.fetch_leads("follow_up")
        
        for record in leads:
            fields = record['fields']
            last_sent = datetime.fromisoformat(fields.get('Last Email Sent', '2024-01-01'))
            days_since = (datetime.now().date() - last_sent.date()).days
            attempts = fields.get('Follow-up Attempts', 0)
            
            # Determine if follow-up is due
            follow_up_schedule = [3, 7, 14]  # Days after last email
            if days_since >= follow_up_schedule[min(attempts, len(follow_up_schedule) - 1)]:
                print(f"📧 Sending follow-up #{attempts + 1} to {fields.get('Lead Name', 'Unknown')}")
                
                email_content = self.generate_follow_up_email(fields, attempts + 1)
                lines = email_content.split('\n')
                subject = f"Re: {lines[0]}"
                body = '\n'.join(lines[1:])
                
                if self.send_email(fields['Email'], subject, body):
                    self.kpis["emails_sent"] += 1
                    
                    # Update Airtable
                    self.update_lead_status(record['id'], {
                        "Last Email Sent": datetime.now().date().isoformat(),
                        "Follow-up Attempts": attempts + 1,
                        "AI Suggested Next Step": f"Follow-up #{attempts + 1} sent; monitor for reply"
                    })
                    
                    print(f"✅ Follow-up sent successfully")
                    time.sleep(2)
    
    def calculate_kpis(self) -> Dict:
        """Calculate and return comprehensive KPIs"""
        all_leads = self.fetch_leads()
        
        total_leads = len(all_leads)
        emails_sent = sum(1 for lead in all_leads if lead['fields'].get('Email Sent?', False))
        
        # Reply classification counts
        interested_count = sum(1 for lead in all_leads if lead['fields'].get('Reply Status') == 'Interested')
        later_count = sum(1 for lead in all_leads if lead['fields'].get('Reply Status') == 'Later')
        not_now_count = sum(1 for lead in all_leads if lead['fields'].get('Reply Status') == 'Not Now')
        wrong_person_count = sum(1 for lead in all_leads if lead['fields'].get('Reply Status') == 'Wrong Person')
        meeting_booked_count = sum(1 for lead in all_leads if lead['fields'].get('Reply Status') == 'Meeting Booked')
        
        # Calendly tracking
        calendly_clicks = sum(1 for lead in all_leads if lead['fields'].get('Calendly Clicked', False))
        demos_booked = sum(1 for lead in all_leads if lead['fields'].get('Demo Booked?', False))
        
        # Follow-up metrics
        follow_up_attempts = sum(lead['fields'].get('Follow-up Attempts', 0) for lead in all_leads)
        
        return {
            "total_leads": total_leads,
            "emails_sent": emails_sent,
            "reply_breakdown": {
                "interested": interested_count,
                "later": later_count,
                "not_now": not_now_count,
                "wrong_person": wrong_person_count,
                "meeting_booked": meeting_booked_count
            },
            "calendly_metrics": {
                "clicks": calendly_clicks,
                "demos_booked": demos_booked,
                "conversion_rate": (demos_booked / calendly_clicks * 100) if calendly_clicks > 0 else 0
            },
            "follow_up_metrics": {
                "total_attempts": follow_up_attempts,
                "avg_attempts_per_lead": follow_up_attempts / emails_sent if emails_sent > 0 else 0
            },
            "overall_rates": {
                "reply_rate": ((interested_count + later_count + meeting_booked_count) / emails_sent * 100) if emails_sent > 0 else 0,
                "meeting_rate": (meeting_booked_count / emails_sent * 100) if emails_sent > 0 else 0,
                "demo_rate": (demos_booked / emails_sent * 100) if emails_sent > 0 else 0
            }
        }
    
    def run(self):
        """Main execution loop"""
        print("🚀 Starting Niya Sales Agent...")
        
        try:
            # Process new leads
            self.process_new_leads()
            
            # Process follow-ups
            self.process_follow_ups()
            
            # Calculate and display KPIs
            kpis = self.calculate_kpis()
            print("\n📊 Niya Sales Agent KPI Dashboard")
            print("=" * 50)
            print(f"📈 Overall Metrics:")
            print(f"   Total Leads: {kpis['total_leads']}")
            print(f"   Emails Sent: {kpis['emails_sent']}")
            print(f"   Reply Rate: {kpis['overall_rates']['reply_rate']:.1f}%")
            print(f"   Meeting Rate: {kpis['overall_rates']['meeting_rate']:.1f}%")
            print(f"   Demo Rate: {kpis['overall_rates']['demo_rate']:.1f}%")
            
            print(f"\n📧 Reply Breakdown:")
            print(f"   Interested: {kpis['reply_breakdown']['interested']}")
            print(f"   Later: {kpis['reply_breakdown']['later']}")
            print(f"   Not Now: {kpis['reply_breakdown']['not_now']}")
            print(f"   Wrong Person: {kpis['reply_breakdown']['wrong_person']}")
            print(f"   Meeting Booked: {kpis['reply_breakdown']['meeting_booked']}")
            
            print(f"\n📅 Calendly Metrics:")
            print(f"   Clicks: {kpis['calendly_metrics']['clicks']}")
            print(f"   Demos Booked: {kpis['calendly_metrics']['demos_booked']}")
            print(f"   Conversion Rate: {kpis['calendly_metrics']['conversion_rate']:.1f}%")
            
            print(f"\n🔄 Follow-up Metrics:")
            print(f"   Total Attempts: {kpis['follow_up_metrics']['total_attempts']}")
            print(f"   Avg Attempts/Lead: {kpis['follow_up_metrics']['avg_attempts_per_lead']:.1f}")
            
            # Log KPIs to the KPIs base
            self.log_kpis(kpis)
            
        except Exception as e:
            print(f"❌ Error in main execution: {e}")

def main():
    agent = NiyaSalesAgent()
    agent.run()

if __name__ == "__main__":
    main()
