# 🔗 Dual Airtable Base Setup for Niya Sales Agent

## ✅ **Your Airtable Bases:**

### **📊 Leads Base** (Main CRM)
- **Base ID**: `appzukRazDqAm3RwI`
- **Table**: `Leads`
- **Purpose**: Lead management, email tracking, reply classification
- **Template**: `niya_leads_template.csv`

### **📈 KPIs Base** (Analytics Dashboard)
- **Base ID**: `app5MfJmA49we1vjM`
- **Table**: `Weekly KPIs`
- **Purpose**: Weekly performance tracking, metrics aggregation
- **Template**: `niya_weekly_kpis_template.csv`

## 🚀 **Quick Setup:**

### **1. Create Your .env File**
```bash
copy env_template.txt .env
```

### **2. Edit Your .env File**
```env
# Airtable Configuration
AIRTABLE_TOKEN=patR0jIjjm7kQfHt.4156ae0cff4adf236b26e34240c109b122d7b722cecfa08d95cd4c4a300f284a
LEADS_BASE_ID=appzukRazDqAm3RwI
KPIS_BASE_ID=app5MfJmA49we1vjM

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Calendly Configuration
CALENDLY_LINK=https://calendly.com/niya/15min
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Test Both Connections**
```bash
python test_setup.py
```

## 📊 **Leads Base Structure** (`appzukRazDqAm3RwI`)

### **Required Fields in "Leads" Table:**

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `Lead Name` | Single line text | Contact's full name |
| `Email` | Email | Contact's email address |
| `Company Name` | Single line text | Company name |
| `Role` | Single line text | Job title/position |
| `Industry` | Single select | Technology, Healthcare, etc. |
| `Company Size` | Single select | 1-10, 11-50, 51-200, etc. |
| `Email Sent?` | Checkbox | Whether initial email was sent |
| `Last Email Sent` | Date | Date of last email sent |
| `Reply Status` | Single select | Interested, Later, Not Now, Wrong Person, Meeting Booked |
| `Follow-up Attempts` | Number | Number of follow-up emails sent |
| `Calendly Clicked` | Checkbox | Whether Calendly link was clicked |
| `Demo Booked?` | Checkbox | Whether demo was scheduled |
| `Demo Brief` | Long text | AI-generated briefing for Jayashree |

## 📈 **KPIs Base Structure** (`app5MfJmA49we1vjM`)

### **Required Fields in "Weekly KPIs" Table:**

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `Week Starting` | Date | Start of the week |
| `Total Leads` | Number | Total leads in system |
| `Emails Sent` | Number | Emails sent this week |
| `Interested Replies` | Number | Interested responses |
| `Later Replies` | Number | Later responses |
| `Not Now Replies` | Number | Not interested responses |
| `Wrong Person Replies` | Number | Wrong contact responses |
| `Meetings Booked` | Number | Meetings scheduled |
| `Calendly Clicks` | Number | Calendly link clicks |
| `Demos Booked` | Number | Demos scheduled |
| `Reply Rate` | Number | Percentage reply rate |
| `Meeting Rate` | Number | Percentage meeting rate |
| `Demo Rate` | Number | Percentage demo rate |
| `Total Follow-up Attempts` | Number | Total follow-up emails sent |

## 🔄 **How the System Works:**

### **📥 Lead Processing:**
1. **Agent reads** from Leads base (`appzukRazDqAm3RwI`)
2. **Sends emails** via Gmail API
3. **Updates lead status** in Leads base
4. **Tracks replies** and classifications

### **📊 KPI Logging:**
1. **Calculates metrics** from Leads base data
2. **Logs weekly KPIs** to KPIs base (`app5MfJmA49we1vjM`)
3. **Updates existing weeks** or creates new records
4. **Provides analytics dashboard**

## 🧪 **Testing Your Setup:**

### **Test Both Bases:**
```bash
python test_setup.py
```

### **Test Lead Processing:**
```bash
python niya_agent.py
```

### **Test Demo Briefs:**
```bash
python generate_demo_briefs.py
```

## 📊 **Expected Output:**

When you run the agent, you'll see:
```
🔄 Processing new leads...
📧 Sending email to John Doe at TechCorp
✅ Email sent successfully to john@techcorp.com

📊 Niya Sales Agent KPI Dashboard
==================================================
📈 Overall Metrics:
   Total Leads: 25
   Emails Sent: 15
   Reply Rate: 23.3%
   Meeting Rate: 6.7%
   Demo Rate: 3.3%

📧 Reply Breakdown:
   Interested: 2
   Later: 1
   Not Now: 1
   Wrong Person: 0
   Meeting Booked: 1

📅 Calendly Metrics:
   Clicks: 3
   Demos Booked: 1
   Conversion Rate: 33.3%

🔄 Follow-up Metrics:
   Total Attempts: 8
   Avg Attempts/Lead: 0.5

📊 Logged KPIs for week starting 2024-01-15
```

## 🔒 **Security & Permissions:**

- ✅ **Personal Access Token** has limited scope
- ✅ **Read/Write access** to both bases
- ✅ **No sensitive data** in code
- ✅ **Environment variables** for security

## 🎯 **Next Steps:**

1. **Set up both Airtable bases** with the required fields
2. **Add test leads** to the Leads base
3. **Run the agent** to start automation
4. **Monitor KPIs** in the analytics base
5. **Generate demo briefs** for booked meetings

## 📈 **Benefits of Dual-Base System:**

- **📊 Clean separation** of operational data and analytics
- **📈 Historical tracking** of weekly performance
- **🔍 Easy reporting** and dashboard creation
- **🔄 Automated KPI logging** without manual work
- **📋 Scalable architecture** for future features

---

**Your dual-base Niya Sales Agent is ready for production! 🚀** 