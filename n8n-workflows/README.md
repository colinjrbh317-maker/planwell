# PlanWell n8n Workflows

This folder contains everything you need to set up automated notifications for your PlanWell website.

## 📦 What's Included

### Workflows (JSON files - already imported ✅)
- `contact-form-workflow.json` - Contact form notifications
- `webinar-registration-workflow.json` - Webinar registration notifications

### Setup Scripts
- `setup_google_sheets.py` - **Python script to create Google Sheets** (recommended)
- `google-sheets-setup.gs` - Google Apps Script alternative
- `setup.sh` - Automated setup shell script
- `requirements.txt` - Python dependencies

### Documentation
- `README.md` - This file
- `PYTHON-SETUP.md` - **Step-by-step Python setup guide** ⭐
- `SETUP-GUIDE.md` - Complete manual setup guide
- `QUICK-START.md` - Quick reference

---

## 🚀 Quick Start (3 Steps)

Since you've already imported the workflows into n8n, you just need to:

### **Step 1: Get Google Cloud Credentials** (2 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Google Sheets API → Create OAuth credentials (Desktop app)
3. Download `credentials.json` and place it in this folder

**Detailed instructions:** See [PYTHON-SETUP.md](./PYTHON-SETUP.md#step-2-get-google-cloud-credentials)

### **Step 2: Run the Setup Script** (1 minute)

```bash
cd "/Users/colinryan/PLAN WELL/planwell-site/n8n-workflows"
chmod +x setup.sh
./setup.sh
```

Or run Python script directly:
```bash
pip install -r requirements.txt
python setup_google_sheets.py
```

This will:
- ✅ Create both Google Sheets with proper formatting
- ✅ Print the Sheet IDs you need
- ✅ Save IDs to `sheet_ids.json`

### **Step 3: Configure n8n** (2 minutes per workflow)

For each workflow in n8n:

1. **Click "Add to Google Sheet" node**
   - Connect Google Sheets OAuth
   - Paste Sheet ID (from script output)
   - Set Sheet Name to `Sheet1`

2. **Click "Send Email Notification" node**
   - Connect Gmail OAuth
   - Verify recipients

3. **Activate workflow** (toggle to ON)

4. **Copy webhook URL** for your website

**Detailed instructions:** See [PYTHON-SETUP.md](./PYTHON-SETUP.md#step-4-configure-n8n-workflows)

---

## 📋 What Each Workflow Does

### 1. Contact Form Workflow
**Webhook:** `https://colinryan17.app.n8n.cloud/webhook/contact`

**Flow:**
```
Website Form → n8n Webhook → Google Sheets → Email → Response
```

**Data Captured:**
- First Name, Last Name
- Email, Phone
- Message
- Submitted At
- Source

**Notifications sent to:**
- david.fei@planwellfp.com
- brennan.rhule@planwellfp.com

---

### 2. Webinar Registration Workflow
**Webhook:** `https://colinryan17.app.n8n.cloud/webhook/webinar`

**Flow:**
```
Website Form → n8n Webhook → Google Sheets → Email → Response
```

**Data Captured:**
- First Name, Last Name
- Email
- Federal Agency
- Retirement Timeline
- Submitted At
- Source

**Notifications sent to:**
- david.fei@planwellfp.com
- brennan.rhule@planwellfp.com

---

## 🧪 Testing

After setup, test with these curl commands:

### Test Contact Form:
```bash
curl -X POST https://colinryan17.app.n8n.cloud/webhook/contact \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","phone":"555-0123","message":"Test message","submitted_at":"2025-12-17T18:00:00Z","source":"Test"}'
```

### Test Webinar:
```bash
curl -X POST https://colinryan17.app.n8n.cloud/webhook/webinar \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","agency":"Test Agency","timeline":"1-2 years","submitted_at":"2025-12-17T18:00:00Z","source":"Test"}'
```

**Expected response:**
```json
{"success": true, "message": "Contact form received"}
```

---

## 📁 File Structure

```
n8n-workflows/
├── README.md                              # This file
├── PYTHON-SETUP.md                        # Step-by-step Python guide ⭐
├── QUICK-START.md                         # Quick reference
├── SETUP-GUIDE.md                         # Complete manual guide
│
├── contact-form-workflow.json             # Contact form workflow ✅
├── webinar-registration-workflow.json     # Webinar workflow ✅
│
├── setup_google_sheets.py                 # Python setup script ⭐
├── requirements.txt                       # Python dependencies
├── setup.sh                               # Automated setup script
├── google-sheets-setup.gs                 # Apps Script alternative
│
├── credentials.json                       # Your OAuth creds (create this)
├── token.json                             # Auto-generated auth token
└── sheet_ids.json                         # Auto-generated Sheet IDs
```

---

## 🔐 Security Notes

**Do NOT commit these files to git:**
- `credentials.json` - Your OAuth credentials
- `token.json` - Your access token
- `sheet_ids.json` - Contains your Sheet IDs

Add to `.gitignore`:
```
credentials.json
token.json
sheet_ids.json
```

---

## 📚 Documentation

- **For Python setup:** Read [PYTHON-SETUP.md](./PYTHON-SETUP.md)
- **For quick reference:** Read [QUICK-START.md](./QUICK-START.md)
- **For detailed manual setup:** Read [SETUP-GUIDE.md](./SETUP-GUIDE.md)

---

## ❓ Troubleshooting

### "credentials.json not found"
→ See [PYTHON-SETUP.md Step 2](./PYTHON-SETUP.md#step-2-get-google-cloud-credentials)

### "Module not found"
→ Run: `pip install -r requirements.txt`

### "Webhook not working"
→ Make sure workflow is **Active** in n8n (toggle to ON)

### "Email not sent"
→ Check Gmail OAuth credentials in n8n

---

## ✅ Final Checklist

- [ ] Workflows imported into n8n ✅ (You did this!)
- [ ] Python dependencies installed
- [ ] Google Cloud credentials downloaded
- [ ] Setup script run successfully
- [ ] Sheet IDs obtained
- [ ] n8n workflows configured with Sheet IDs
- [ ] Google Sheets OAuth connected in n8n
- [ ] Gmail OAuth connected in n8n
- [ ] Both workflows activated
- [ ] Webhook URLs copied
- [ ] Test submissions successful

---

## 🎉 Need Help?

1. Check [PYTHON-SETUP.md](./PYTHON-SETUP.md) for step-by-step instructions
2. Review the troubleshooting section above
3. Check n8n's Executions tab for error details

---

**Your n8n Instance:** https://colinryan17.app.n8n.cloud/

**Estimated setup time:** 5-10 minutes total
