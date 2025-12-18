# PlanWell n8n Workflows - Quick Start Guide

## 🚀 5-Minute Setup

### Option A: Automated Setup (Recommended)

#### 1. Auto-Create Google Sheets (2 minutes)
```
1. Go to https://script.google.com/
2. Click "New Project"
3. Paste the code from google-sheets-setup.gs
4. Save as "PlanWell Setup"
5. Run setupPlanWellSheets()
6. Grant permissions
7. Copy the Sheet IDs from the logs
```

#### 2. Import n8n Workflows (2 minutes)
```
1. Go to https://colinryan17.app.n8n.cloud/
2. Workflows > + > Import from File
3. Import contact-form-workflow.json
4. Import webinar-registration-workflow.json
```

#### 3. Configure Workflows (1 minute per workflow)
```
For each workflow:
1. Click "Add to Google Sheet" node
   - Connect Google Sheets OAuth
   - Paste Sheet ID
   - Set Sheet Name to "Sheet1"

2. Click "Send Email Notification" node
   - Connect Gmail OAuth
   - Verify recipients

3. Activate workflow (toggle to ON)
4. Copy webhook URL
```

---

### Option B: Manual Setup

#### 1. Create Google Sheets Manually
**Contact Form Sheet:**
```
Columns: First Name | Last Name | Email | Phone | Message | Submitted At | Source
```

**Webinar Sheet:**
```
Columns: First Name | Last Name | Email | Agency | Retirement Timeline | Submitted At | Source
```

#### 2. Follow steps 2-3 from Option A

---

## 📋 Checklist

- [ ] Google Sheets created with correct columns
- [ ] Contact form workflow imported
- [ ] Webinar workflow imported
- [ ] Google Sheets credentials configured
- [ ] Gmail credentials configured
- [ ] Both workflows activated
- [ ] Webhook URLs copied
- [ ] Test submissions successful

---

## 🔗 Important URLs

- **Your n8n Instance:** https://colinryan17.app.n8n.cloud/
- **Google Sheets:** https://sheets.google.com
- **Google Apps Script:** https://script.google.com/

---

## 🧪 Test Commands

### Test Contact Form:
```bash
curl -X POST https://colinryan17.app.n8n.cloud/webhook/contact \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","phone":"555-0123","message":"Test message","submitted_at":"2025-12-17T18:00:00Z","source":"Test"}'
```

### Test Webinar Registration:
```bash
curl -X POST https://colinryan17.app.n8n.cloud/webhook/webinar \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","agency":"Test Agency","timeline":"1-2 years","submitted_at":"2025-12-17T18:00:00Z","source":"Test"}'
```

---

## 📧 Email Recipients

Both workflows send notifications to:
- david.fei@planwellfp.com
- brennan.rhule@planwellfp.com

---

## 🔍 Webhook URLs (after activation)

You'll get URLs like:
- Contact Form: `https://colinryan17.app.n8n.cloud/webhook/contact`
- Webinar: `https://colinryan17.app.n8n.cloud/webhook/webinar`

Use these in your website forms!

---

## ❓ Need Help?

See [SETUP-GUIDE.md](./SETUP-GUIDE.md) for detailed instructions and troubleshooting.

---

**Estimated Total Time:** 5-10 minutes ⏱️
