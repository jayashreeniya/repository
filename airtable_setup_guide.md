# 📋 Airtable Setup Guide for Niya Sales Agent

## 🎯 Complete Field Structure

Create a base called "Niya Sales" with a table called "Leads" containing these fields:

### 📝 Basic Lead Information
| Field Name | Type | Description |
|------------|------|-------------|
| Lead Name | Single line text | Contact's full name |
| Email | Email | Contact's email address |
| Company Name | Single line text | Company name |
| Role | Single line text | Job title/position |
| Industry | Single select | Technology, Healthcare, Finance, etc. |
| Company Size | Single select | 1-10, 11-50, 51-200, 201-1000, 1000+ |
| Website/LinkedIn | URL | Company website or LinkedIn profile |
| Company Description | Long text | Brief company description |

### 📧 Email Campaign Fields
| Field Name | Type | Description |
|------------|------|-------------|
| Email Sent? | Checkbox | Whether initial email was sent |
| Last Email Sent | Date | Date of last email sent |
| Follow-up Attempts | Number | Number of follow-up emails sent |
| Reply Status | Single select | Interested, Later, Not Now, Wrong Person, Meeting Booked |
| Reply Type | Long text | Detailed reply classification |
| Notes/Objections | Long text | Key points from replies or objections |

### 📅 Calendly & Demo Fields
| Field Name | Type | Description |
|------------|------|-------------|
| Calendly Clicked | Checkbox | Whether Calendly link was clicked |
| Demo Booked? | Checkbox | Whether demo was scheduled |
| Demo Date | Date | Scheduled demo date/time |
| Demo Brief | Long text | AI-generated briefing for Jayashree |

### 🎯 Sales Pipeline Fields
| Field Name | Type | Description |
|------------|------|-------------|
| Stage | Single select | New Lead, Contacted, Interested, Demo Scheduled, Won, Lost |
| AI Suggested Next Step | Long text | Next action recommended by AI |
| Lead Source | Single select | LinkedIn, Website, Referral, etc. |
| Priority | Single select | High, Medium, Low |

### 📊 KPI Tracking Fields
| Field Name | Type | Description |
|------------|------|-------------|
| First Contact Date | Date | When first email was sent |
| Last Activity Date | Date | Last interaction date |
| Days in Pipeline | Formula | Days since first contact |
| Conversion Probability | Number | AI-calculated conversion chance (0-100) |

## 🔧 Airtable Setup Steps

### 1. Create the Base
1. Go to [Airtable.com](https://airtable.com)
2. Click "Add a base"
3. Choose "Start from scratch"
4. Name it "Niya Sales"

### 2. Create the Leads Table
1. Rename the first table to "Leads"
2. Add all fields listed above
3. Set up the single select options:

**Industry Options:**
- Technology
- Healthcare
- Finance
- Manufacturing
- Retail
- Education
- Other

**Company Size Options:**
- 1-10 employees
- 11-50 employees
- 51-200 employees
- 201-1000 employees
- 1000+ employees

**Reply Status Options:**
- Interested
- Later
- Not Now
- Wrong Person
- Meeting Booked

**Stage Options:**
- New Lead
- Contacted
- Interested
- Demo Scheduled
- Won
- Lost

**Priority Options:**
- High
- Medium
- Low

### 3. Set Up Views

Create these views for better organization:

#### 📊 Dashboard View
- Group by: Stage
- Sort by: Last Activity Date (descending)
- Filter: Show all records

#### 📧 Email Campaign View
- Filter: Email Sent? = FALSE
- Sort by: Created date (ascending)

#### 🔄 Follow-up View
- Filter: Email Sent? = TRUE AND Reply Status = ""
- Sort by: Last Email Sent (ascending)

#### 📅 Demo Pipeline View
- Filter: Demo Booked? = TRUE
- Sort by: Demo Date (ascending)

#### 🎯 Hot Leads View
- Filter: Reply Status = "Interested" OR Reply Status = "Meeting Booked"
- Sort by: Last Activity Date (descending)

### 4. Set Up Automations (Optional)

#### Auto-update Last Activity
- Trigger: Record updated
- Action: Set Last Activity Date to today

#### Auto-calculate Days in Pipeline
- Trigger: Record updated
- Action: Calculate days since First Contact Date

## 🔗 Integration Setup

### 1. Get API Key
1. Go to [Airtable.com/account](https://airtable.com/account)
2. Click "Generate API key"
3. Copy the key

### 2. Get Base ID
1. Open your base
2. Go to Help > API Documentation
3. Copy the Base ID from the URL

### 3. Update Environment Variables
Add to your `.env` file:
```env
AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=your_base_id_here
```

## 📊 KPI Dashboard Setup

### 1. Create Summary Fields
Add these formula fields for automatic KPI calculation:

**Total Leads:**
```
COUNT()
```

**Emails Sent:**
```
COUNTIF({Email Sent?}, TRUE)
```

**Reply Rate:**
```
IF({Emails Sent} > 0, 
   (COUNTIF({Reply Status}, "Interested") + COUNTIF({Reply Status}, "Later") + COUNTIF({Reply Status}, "Meeting Booked")) / {Emails Sent} * 100, 
   0)
```

**Meeting Rate:**
```
IF({Emails Sent} > 0, 
   COUNTIF({Reply Status}, "Meeting Booked") / {Emails Sent} * 100, 
   0)
```

### 2. Create Dashboard View
- Group by: None
- Add summary fields to the view
- Pin important metrics at the top

## 🚀 Testing the Setup

1. **Add a test lead** with all required fields
2. **Run the test script:**
   ```bash
   python test_setup.py
   ```
3. **Test email generation:**
   ```bash
   python niya_agent.py
   ```
4. **Test demo brief generation:**
   ```bash
   python generate_demo_briefs.py
   ```

## 🔒 Security Best Practices

- ✅ Never share your API key
- ✅ Use environment variables
- ✅ Regularly rotate API keys
- ✅ Monitor API usage
- ✅ Set up field-level permissions if needed

## 📈 Advanced Features

### Webhook Integration
Set up webhooks to automatically trigger actions when:
- New leads are added
- Reply status changes
- Demo is booked

### Multi-user Access
- Add team members with appropriate permissions
- Set up field-level access controls
- Create user-specific views

### Data Export
- Set up automated exports to CSV/Excel
- Integrate with Google Sheets
- Connect to BI tools for advanced analytics

---

**Your Airtable is now ready for the complete Niya Sales Agent automation! 🚀** 