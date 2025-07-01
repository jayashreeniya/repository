# 🤖 Niya AI Sales Agent

An intelligent, automated B2B sales agent powered by GPT-4, Airtable, and Gmail API. This agent automatically generates personalized cold emails, manages follow-up sequences, classifies replies, and tracks KPIs.

## ✨ Features

- **🤖 AI-Powered Email Generation**: Personalized cold emails using GPT-4
- **📧 Automated Follow-ups**: Smart follow-up sequences at 3, 7, and 14 days
- **📊 Reply Classification**: Automatically categorizes responses (Positive/Negative/Neutral/Meeting Booked)
- **📈 KPI Tracking**: Real-time metrics including reply rates and meeting bookings
- **🔗 Calendly Integration**: Automatic Calendly link inclusion and click tracking
- **📋 Airtable Integration**: Seamless lead management and status updates
- **⚡ Rate Limiting**: Built-in email throttling to avoid spam filters

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd niya-sales-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
```bash
# Copy the template
cp env_template.txt .env

# Edit .env with your actual values
nano .env
```

### 4. Configure Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create a Service Account
5. Download the JSON key file as `gmail-service.json`
6. Place it in the project directory
7. Share your Gmail with the service account email

### 5. Set Up Airtable
1. Create a base with a "Leads" table
2. Add these fields:
   - Lead Name (Single line text)
   - Email (Email)
   - Company Name (Single line text)
   - Role (Single line text)
   - Company Description (Long text)
   - Stage (Single select: Series A, Series B, Series C, etc.)
   - Email Sent? (Checkbox)
   - Last Email Sent (Date)
   - Reply Status (Single select: Positive, Negative, Neutral, Meeting Booked)
   - Follow-up Attempts (Number)
   - AI Suggested Next Step (Long text)
   - Notes/Objections (Long text)

### 6. Run the Agent
```bash
python niya_agent.py
```

## 📋 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AIRTABLE_API_KEY` | Your Airtable API key | ✅ |
| `AIRTABLE_BASE_ID` | Your Airtable base ID | ✅ |
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ |
| `CALENDLY_LINK` | Your Calendly booking link | ❌ |
| `FOLLOW_UP_SCHEDULE` | Days for follow-ups (comma-separated) | ❌ |
| `EMAIL_DELAY` | Seconds between emails | ❌ |
| `MAX_FOLLOW_UPS` | Maximum follow-up attempts | ❌ |

## 🔧 Configuration

### Follow-up Schedule
The agent automatically sends follow-ups at 3, 7, and 14 days after the initial email. You can customize this in the `.env` file:

```env
FOLLOW_UP_SCHEDULE=3,7,14
```

### Rate Limiting
To avoid triggering spam filters, emails are sent with delays:

```env
EMAIL_DELAY=2
```

## 📊 KPI Dashboard

The agent tracks these key metrics:

- **Total Leads**: Number of leads in your Airtable
- **Emails Sent**: Total emails sent (initial + follow-ups)
- **Positive Replies**: Leads with positive responses
- **Meetings Booked**: Confirmed meetings
- **Reply Rate**: Percentage of positive replies
- **Meeting Rate**: Percentage of meetings booked

## 🤖 How It Works

### 1. Lead Processing
- Fetches leads from Airtable where "Email Sent?" is false
- Generates personalized cold emails using GPT-4
- Sends emails via Gmail API
- Updates Airtable with status

### 2. Follow-up Management
- Monitors leads that need follow-ups
- Sends follow-up emails at scheduled intervals
- Tracks follow-up attempts
- Updates lead status

### 3. Reply Classification
- Analyzes incoming replies using GPT-4
- Categorizes responses automatically
- Suggests next actions
- Updates lead status in Airtable

## 🔄 Automation

### Running as a Service
To run the agent continuously:

```bash
# Using cron (Linux/Mac)
crontab -e
# Add: 0 */4 * * * cd /path/to/niya-sales-agent && python niya_agent.py

# Using Windows Task Scheduler
# Create a scheduled task to run every 4 hours
```

### Docker Support
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "niya_agent.py"]
```

## 🛠️ Troubleshooting

### Common Issues

1. **Gmail API Error**: Ensure service account has proper permissions
2. **Airtable Connection**: Verify API key and base ID
3. **OpenAI Rate Limits**: Check your API usage and limits
4. **Email Delivery**: Check spam folder and sender reputation

### Debug Mode
Add debug logging by modifying the script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security

- Never commit your `.env` file or `gmail-service.json`
- Use environment variables for all sensitive data
- Regularly rotate API keys
- Monitor API usage and costs

## 📈 Advanced Features

### Custom Email Templates
Modify the `generate_cold_email()` method to use custom templates:

```python
def generate_cold_email(self, fields: Dict) -> str:
    # Your custom email generation logic
    pass
```

### Integration with CRM
Extend the agent to sync with your CRM:

```python
def sync_to_crm(self, lead_data: Dict):
    # Integrate with Salesforce, HubSpot, etc.
    pass
```

### Webhook Support
Add webhook endpoints for real-time updates:

```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/webhook/calendly', methods=['POST'])
def calendly_webhook():
    # Handle Calendly booking notifications
    pass
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

---

**Made with ❤️ for Niya Sales Team**
