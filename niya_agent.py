import os, time, base64
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from airtable import Airtable
from googleapiclient.discovery import build
from google.oauth2 import service_account
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE = "Leads"
CALENDLY_LINK = os.getenv("CALENDLY_LINK", "https://calendly.com/niya/15min")

# Initialize services
GMAIL_SERVICE_ACC = service_account.Credentials.from_service_account_file(
    "gmail-service.json",
    scopes=["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.readonly"]
)
GMAIL = build("gmail", "v1", credentials=GMAIL_SERVICE_ACC)
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
at = Airtable(BASE_ID, TABLE, AIRTABLE_API_KEY)

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
            formula = "AND({Email Sent?}=FALSE, {Email}!='')"
        elif status_filter == "follow_up":
            formula = "AND({Email Sent?}=TRUE, {Last Email Sent}!='', {Reply Status}='')"
        elif status_filter == "positive":
            formula = "{Reply Status}='Positive'"
        else:
            formula = ""
        
        return at.get_all(formula=formula) if formula else at.get_all()
    
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
        - Positive: Interested, wants to learn more, asks questions, books meeting
        - Negative: Not interested, objections, declines
        - Neutral: Acknowledges receipt, asks for more info, needs time
        - Meeting Booked: Confirms meeting or calendar booking
        
        Reply: {reply_text}
        
        Return JSON format:
        {{
            "category": "Positive/Negative/Neutral/Meeting Booked",
            "confidence": 0.95,
            "key_points": ["point1", "point2"],
            "next_action": "suggested next step"
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
        """Send email via Gmail API"""
        try:
            msg = f"To: {to}\r\nSubject: {subject}\r\n\r\n{body}"
            raw = base64.urlsafe_b64encode(msg.encode()).decode()
            GMAIL.users().messages().send(userId="me", body={"raw": raw}).execute()
            return True
        except Exception as e:
            print(f"Error sending email to {to}: {e}")
            return False
    
    def check_calendly_clicks(self, email: str) -> bool:
        """Check if Calendly link was clicked (simplified version)"""
        # In a real implementation, you'd integrate with Calendly webhooks
        # For now, we'll simulate this based on reply content
        return "calendly" in email.lower() or "book" in email.lower()
    
    def update_lead_status(self, record_id: str, updates: Dict):
        """Update lead status in Airtable"""
        try:
            at.update(record_id, updates)
        except Exception as e:
            print(f"Error updating record {record_id}: {e}")
    
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
        """Calculate and return KPIs"""
        all_leads = self.fetch_leads()
        
        total_leads = len(all_leads)
        emails_sent = sum(1 for lead in all_leads if lead['fields'].get('Email Sent?', False))
        positive_replies = sum(1 for lead in all_leads if lead['fields'].get('Reply Status') == 'Positive')
        meetings_booked = sum(1 for lead in all_leads if lead['fields'].get('Reply Status') == 'Meeting Booked')
        
        return {
            "total_leads": total_leads,
            "emails_sent": emails_sent,
            "positive_replies": positive_replies,
            "meetings_booked": meetings_booked,
            "reply_rate": (positive_replies / emails_sent * 100) if emails_sent > 0 else 0,
            "meeting_rate": (meetings_booked / emails_sent * 100) if emails_sent > 0 else 0
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
            print("\n📊 Current KPIs:")
            print(f"   Total Leads: {kpis['total_leads']}")
            print(f"   Emails Sent: {kpis['emails_sent']}")
            print(f"   Positive Replies: {kpis['positive_replies']}")
            print(f"   Meetings Booked: {kpis['meetings_booked']}")
            print(f"   Reply Rate: {kpis['reply_rate']:.1f}%")
            print(f"   Meeting Rate: {kpis['meeting_rate']:.1f}%")
            
        except Exception as e:
            print(f"❌ Error in main execution: {e}")

def main():
    agent = NiyaSalesAgent()
    agent.run()

if __name__ == "__main__":
    main()
