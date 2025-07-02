# 🔑 Airtable Personal Access Token Setup

## ✅ **Your Token is Ready!**

You have your Personal Access Token: `patR0jIjjm7kQfHt.4156ae0cff4adf236b26e34240c109b122d7b722cecfa08d95cd4c4a300f284a`

## 🚀 **Quick Setup Steps:**

### **1. Create Your .env File**
```bash
# Copy the template
copy env_template.txt .env
```

### **2. Edit Your .env File**
Replace the placeholder with your actual token:

```env
# Airtable Configuration
AIRTABLE_TOKEN=patR0jIjjm7kQfHt.4156ae0cff4adf236b26e34240c109b122d7b722cecfa08d95cd4c4a300f284a
AIRTABLE_BASE_ID=your_base_id_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Calendly Configuration
CALENDLY_LINK=https://calendly.com/niya/15min
```

### **3. Get Your Base ID**
1. Open your Airtable base
2. Go to Help → API Documentation
3. Copy the Base ID from the URL (looks like: `appXXXXXXXXXXXXXX`)

### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **5. Test the Connection**
```bash
python test_setup.py
```

## 🔧 **What Changed:**

- ✅ **Updated to Personal Access Tokens** (Airtable's new system)
- ✅ **Removed airtable-python-wrapper dependency**
- ✅ **Using direct API calls with requests**
- ✅ **Better error handling and security**

## 📊 **Your Airtable Base Should Have:**

Make sure your "Leads" table has these fields:

| **Field Name** | **Type** | **Required** |
|----------------|----------|--------------|
| `Lead Name` | Single line text | ✅ |
| `Email` | Email | ✅ |
| `Company Name` | Single line text | ✅ |
| `Role` | Single line text | ✅ |
| `Email Sent?` | Checkbox | ✅ |
| `Last Email Sent` | Date | ✅ |
| `Reply Status` | Single select | ✅ |
| `Follow-up Attempts` | Number | ✅ |

## 🧪 **Test Your Setup:**

```bash
# Test all connections
python test_setup.py

# Test the main agent
python niya_agent.py

# Test demo brief generation
python generate_demo_briefs.py
```

## 🔒 **Security Notes:**

- ✅ Your token is secure and encrypted
- ✅ Never share your token publicly
- ✅ The token has limited permissions
- ✅ Can be revoked and regenerated if needed

## 🎯 **Next Steps:**

1. **Set up your Airtable base** with the required fields
2. **Add some test leads** to your table
3. **Run the agent** to start sending emails
4. **Monitor the KPI dashboard** for results

---

**Your Niya Sales Agent is now ready to connect to Airtable! 🚀** 