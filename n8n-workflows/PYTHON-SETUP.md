# Python Google Sheets Setup - Step by Step

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Python Dependencies

```bash
cd "/Users/colinryan/PLAN WELL/planwell-site/n8n-workflows"
pip install -r requirements.txt
```

Or install manually:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

### Step 2: Get Google Cloud Credentials

#### 2.1 Create/Select a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Name it: `planwell-n8n` (or any name you prefer)
4. Click **"Create"**

#### 2.2 Enable Google Sheets API

1. In the search bar, type **"Google Sheets API"**
2. Click on **"Google Sheets API"**
3. Click **"Enable"**

#### 2.3 Create OAuth 2.0 Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. If prompted, click **"Configure Consent Screen"**:
   - Choose **"External"** (unless you have a Google Workspace)
   - Fill in:
     - App name: `PlanWell Sheets Setup`
     - User support email: Your email
     - Developer contact: Your email
   - Click **"Save and Continue"**
   - Skip "Scopes" (click **"Save and Continue"**)
   - Add yourself as a test user
   - Click **"Save and Continue"**

4. Now create the OAuth client:
   - Application type: **"Desktop app"**
   - Name: `PlanWell Desktop Client`
   - Click **"Create"**

5. **Download the JSON file**:
   - Click the **download icon** (⬇️) next to your new credential
   - Save it as `credentials.json`

#### 2.4 Move credentials.json

Move the downloaded file to your n8n-workflows folder:

```bash
# If downloaded to Downloads folder:
mv ~/Downloads/credentials.json "/Users/colinryan/PLAN WELL/planwell-site/n8n-workflows/"
```

Or just drag and drop it into the `n8n-workflows` folder.

---

### Step 3: Run the Setup Script

```bash
cd "/Users/colinryan/PLAN WELL/planwell-site/n8n-workflows"
python setup_google_sheets.py
```

**What happens:**
1. A browser window will open
2. Choose your Google account
3. Click **"Advanced"** → **"Go to PlanWell Sheets Setup (unsafe)"**
   - This is safe - it's your own app!
4. Click **"Continue"**
5. Grant permissions
6. The script will:
   - Create both Google Sheets
   - Format them with headers
   - Print the Sheet IDs
   - Save IDs to `sheet_ids.json`

**Expected output:**
```
============================================================
PlanWell Google Sheets Setup
============================================================

📋 Creating Contact Form Sheet...
✅ Contact Form Sheet Created!
   Sheet ID: 1abc123xyz456...
   URL: https://docs.google.com/spreadsheets/d/1abc123xyz456.../edit

🎓 Creating Webinar Registration Sheet...
✅ Webinar Registration Sheet Created!
   Sheet ID: 1def789uvw012...
   URL: https://docs.google.com/spreadsheets/d/1def789uvw012.../edit

============================================================
✨ SETUP COMPLETE!
============================================================
```

---

### Step 4: Configure n8n Workflows

You mentioned you already imported the JSON files into n8n. Now you need to configure them:

#### For EACH workflow (Contact Form & Webinar):

1. **Open the workflow in n8n**

2. **Click the "Add to Google Sheet" node**
   - Click **"Credential for Google Sheets"**
   - Click **"Create New Credential"**
   - Click **"Sign in with Google"**
   - Choose your Google account
   - Grant permissions
   - In the **Document ID** field: Paste the Sheet ID from the script output
   - In the **Sheet Name** field: Type `Sheet1`

3. **Click the "Send Email Notification" node**
   - Click **"Credential for Gmail"**
   - Click **"Create New Credential"**
   - Click **"Sign in with Google"**
   - Choose your Gmail account
   - Grant permissions
   - Verify recipients are correct:
     - `david.fei@planwellfp.com`
     - `brennan.rhule@planwellfp.com`

4. **Save the workflow** (click Save button)

5. **Activate the workflow** (toggle switch to ON)

6. **Copy the webhook URL**:
   - Click the "Webhook" node
   - Copy the **Production URL**
   - Should look like: `https://colinryan17.app.n8n.cloud/webhook/contact`

---

### Step 5: Test Your Workflows

#### Test Contact Form:
```bash
curl -X POST https://colinryan17.app.n8n.cloud/webhook/contact \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "phone": "555-0123",
    "message": "This is a test message",
    "submitted_at": "2025-12-17T18:00:00Z",
    "source": "Manual Test"
  }'
```

#### Test Webinar Registration:
```bash
curl -X POST https://colinryan17.app.n8n.cloud/webhook/webinar \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "agency": "Test Agency",
    "timeline": "1-2 years",
    "submitted_at": "2025-12-17T18:00:00Z",
    "source": "Manual Test"
  }'
```

**After testing, verify:**
- ✅ New row appears in Google Sheets
- ✅ Email received by david.fei@ and brennan.rhule@
- ✅ Response: `{"success": true, "message": "..."}`

---

## 📁 Files Created

After running the script, you'll have:

- `credentials.json` - Your Google OAuth credentials (keep private!)
- `token.json` - Your access token (auto-generated, keep private!)
- `sheet_ids.json` - Sheet IDs for easy reference

**⚠️ Important:** Add these to `.gitignore` if you're using git:
```
credentials.json
token.json
sheet_ids.json
```

---

## 🔍 Troubleshooting

### "credentials.json not found"
- Make sure you downloaded the OAuth credentials from Google Cloud
- Ensure it's named exactly `credentials.json`
- Place it in the n8n-workflows folder

### "Access denied" or "Permission denied"
- Make sure you enabled Google Sheets API in Google Cloud Console
- Try deleting `token.json` and running the script again

### "Module not found"
- Run: `pip install -r requirements.txt`
- Or: `pip3 install -r requirements.txt` (if using Python 3)

### "Port already in use"
- The OAuth flow uses port 8080 by default
- Close any other apps using that port
- Or modify the script (change `port=0` to `port=8081`)

---

## ✅ Checklist

- [ ] Python 3 installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] OAuth credentials created and downloaded
- [ ] `credentials.json` in n8n-workflows folder
- [ ] Script run successfully
- [ ] Sheet IDs copied
- [ ] Both n8n workflows configured with Sheet IDs
- [ ] Google Sheets OAuth connected in n8n
- [ ] Gmail OAuth connected in n8n
- [ ] Both workflows activated
- [ ] Test submissions successful

---

## 🎉 Done!

Your workflows are now live and ready to receive form submissions!

**Webhook URLs to use in your website:**
- Contact Form: `https://colinryan17.app.n8n.cloud/webhook/contact`
- Webinar: `https://colinryan17.app.n8n.cloud/webhook/webinar`
