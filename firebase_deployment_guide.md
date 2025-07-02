# 🔥 Firebase Function Deployment Guide

## 📁 **Firebase Function Structure**

```
firebase_functions/
├── main.py              # Flask app with /generate-brief endpoint
├── requirements.txt     # Dependencies for Firebase
└── env_template.txt     # Environment variables template
```

## 🚀 **Deployment Steps**

### **1. Install Firebase CLI**
```bash
npm install -g firebase-tools
```

### **2. Login to Firebase**
```bash
firebase login
```

### **3. Initialize Firebase Project**
```bash
firebase init functions
```

### **4. Replace Firebase Function Files**
Replace the contents of your `functions/` directory with the files from `firebase_functions/`:

```bash
# Copy the main function
copy firebase_functions\main.py functions\main.py

# Copy requirements
copy firebase_functions\requirements.txt functions\requirements.txt

# Copy environment template
copy firebase_functions\env_template.txt functions\.env
```

### **5. Configure Environment Variables**
Edit `functions/.env`:
```env
AIRTABLE_TOKEN=patR0jIjjm7kQfHt.4156ae0cff4adf236b26e34240c109b122d7b722cecfa08d95cd4c4a300f284a
LEADS_BASE_ID=appzukRazDqAm3RwI
OPENAI_API_KEY=your_openai_api_key_here
```

### **6. Deploy to Firebase**
```bash
firebase deploy --only functions
```

## 🔗 **Airtable Button Setup**

### **1. Get Your Firebase Function URL**
After deployment, you'll get a URL like:
```
https://us-central1-YOUR_PROJECT.cloudfunctions.net/firebase_function
```

### **2. Create Airtable Button**
In your Airtable "Leads" table, add a button field with this URL:
```
https://us-central1-YOUR_PROJECT.cloudfunctions.net/firebase_function/generate-brief?recordId={{RECORD_ID()}}
```

### **3. Button Configuration**
- **Button Label**: "Generate Demo Brief"
- **Button Style**: Primary (or your preference)
- **URL**: Use the formula above

## 🧪 **Testing the Function**

### **1. Test Locally**
```bash
cd functions
python main.py
```

### **2. Test Endpoint**
```bash
curl "http://localhost:8080/generate-brief?recordId=YOUR_RECORD_ID"
```

### **3. Test Health Check**
```bash
curl "http://localhost:8080/health"
```

## 📊 **Function Features**

### **✅ What It Does:**
- **Fetches lead data** from Airtable using record ID
- **Generates personalized demo brief** using GPT-4
- **Updates the lead record** with the generated brief
- **Returns success/error response** to Airtable

### **🔧 API Endpoints:**
- `GET /generate-brief?recordId=RECORD_ID` - Generate brief for specific lead
- `POST /generate-brief` - Generate brief (JSON body with recordId)
- `GET /health` - Health check endpoint
- `GET /` - Service information

### **📝 Response Format:**
```json
{
  "success": true,
  "recordId": "recXXXXXXXXXXXXXX",
  "leadName": "John Doe",
  "companyName": "TechCorp",
  "brief": "Generated demo brief content...",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🔒 **Security & Permissions**

### **Firebase Security Rules:**
```javascript
// functions/.firebaserc
{
  "functions": {
    "source": "functions"
  }
}
```

### **Environment Variables:**
- ✅ **AIRTABLE_TOKEN** - Your Personal Access Token
- ✅ **LEADS_BASE_ID** - Your Leads base ID
- ✅ **OPENAI_API_KEY** - Your OpenAI API key

## 🎯 **Usage Workflow**

### **1. Lead Gets Demo Booked**
- Sales team marks "Demo Booked?" = TRUE in Airtable

### **2. Generate Brief**
- Click "Generate Demo Brief" button in Airtable
- Function fetches lead data and generates brief
- Brief is automatically saved to the lead record

### **3. Jayashree Gets Brief**
- Brief appears in "Demo Brief" field
- Ready for the demo call

## 🔧 **Troubleshooting**

### **Common Issues:**

**1. Function Not Deploying:**
```bash
# Check Firebase CLI version
firebase --version

# Clear cache and retry
firebase logout
firebase login
firebase deploy --only functions
```

**2. Environment Variables Not Working:**
```bash
# Set environment variables in Firebase console
firebase functions:config:set airtable.token="YOUR_TOKEN"
firebase functions:config:set airtable.base_id="YOUR_BASE_ID"
firebase functions:config:set openai.api_key="YOUR_API_KEY"
```

**3. Airtable Button Not Working:**
- Check the URL format
- Verify record ID is being passed correctly
- Test the function URL directly

### **Debug Mode:**
```bash
# View function logs
firebase functions:log

# Test function locally
firebase emulators:start --only functions
```

## 📈 **Monitoring & Analytics**

### **Firebase Console:**
- **Functions** → **Logs** - View function execution logs
- **Functions** → **Usage** - Monitor function calls and performance
- **Functions** → **Errors** - Track any errors or failures

### **Airtable Tracking:**
- **Brief Generated** - Boolean field to track if brief was generated
- **Brief Generated Date** - Timestamp of when brief was created
- **Demo Brief** - The actual generated brief content

## 🚀 **Production Deployment**

### **1. Set Production Environment:**
```bash
firebase use production
```

### **2. Deploy to Production:**
```bash
firebase deploy --only functions --project your-production-project
```

### **3. Update Airtable Button:**
Use the production function URL in your Airtable button.

---

**Your Firebase function is ready to generate demo briefs automatically! 🎉** 