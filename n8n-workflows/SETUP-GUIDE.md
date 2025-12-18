# PlanWell n8n Workflows Setup Guide

This guide will help you set up the Google Sheets and import the n8n workflows for PlanWell.

## Part 1: Create Google Sheets

You need to create **2 Google Sheets** with the following structures:

### Sheet 1: Contact Form Submissions

**Create a new Google Sheet named:** `PlanWell Contact Form Submissions`

**Column Headers (in this exact order):**
1. First Name
2. Last Name
3. Email
4. Phone
5. Message
6. Submitted At
7. Source

**Quick Setup:**
1. Go to [Google Sheets](https://sheets.google.com)
2. Click "Blank" to create a new sheet
3. Rename it to "PlanWell Contact Form Submissions"
4. In row 1, add the column headers listed above
5. **Copy the Google Sheet ID from the URL** (it looks like: `1abc...xyz`)
   - Example URL: `https://docs.google.com/spreadsheets/d/1abc123xyz456/edit`
   - The ID is: `1abc123xyz456`

---

### Sheet 2: Webinar Registration Submissions

**Create a new Google Sheet named:** `PlanWell Webinar Registrations`

**Column Headers (in this exact order):**
1. First Name
2. Last Name
3. Email
4. Agency
5. Retirement Timeline
6. Submitted At
7. Source

**Quick Setup:**
1. Go to [Google Sheets](https://sheets.google.com)
2. Click "Blank" to create a new sheet
3. Rename it to "PlanWell Webinar Registrations"
4. In row 1, add the column headers listed above
5. **Copy the Google Sheet ID from the URL**

---

## Part 2: Import Workflows into n8n

### Step 1: Access Your n8n Instance

Go to: https://colinryan17.app.n8n.cloud/

### Step 2: Import Contact Form Workflow

1. In n8n, click **Workflows** in the left sidebar
2. Click the **+** button to create a new workflow
3. Click the **⋮** (three dots menu) in the top right
4. Select **Import from File**
5. Choose the file: `contact-form-workflow.json`
6. The workflow will be imported with 4 nodes:
   - Contact Form Webhook
   - Add to Google Sheet
   - Send Email Notification
   - Respond to Webhook

### Step 3: Configure Contact Form Workflow

After importing, you need to configure the following:

#### A. Configure Google Sheets Node

1. Click on the **"Add to Google Sheet"** node
2. Click **"Create New Credential"** for Google Sheets OAuth2
3. Follow the OAuth flow to connect your Google account
4. Set the **Document ID** to your Contact Form Sheet ID (from Part 1)
5. Set the **Sheet Name** to "Sheet1" (or whatever you named the sheet)
6. Verify the column mappings are correct

#### B. Configure Gmail Node

1. Click on the **"Send Email Notification"** node
2. Click **"Create New Credential"** for Gmail OAuth2
3. Follow the OAuth flow to connect your Gmail account
4. Verify the recipient emails:
   - `david.fei@planwellfp.com`
   - `brennan.rhule@planwellfp.com`

#### C. Activate the Webhook

1. Click on the **"Contact Form Webhook"** node
2. Click **"Listen for Test Event"** or **"Execute Node"**
3. Copy the **Production Webhook URL** (you'll need this for your website)
4. The URL will look like: `https://colinryan17.app.n8n.cloud/webhook/contact`

### Step 4: Import Webinar Registration Workflow

1. Create another new workflow in n8n
2. Click **Import from File**
3. Choose the file: `webinar-registration-workflow.json`
4. The workflow will be imported with 4 nodes:
   - Webinar Registration Webhook
   - Add to Google Sheet
   - Send Email Notification
   - Respond to Webhook

### Step 5: Configure Webinar Registration Workflow

Follow the same steps as the Contact Form workflow:

#### A. Configure Google Sheets Node

1. Click on the **"Add to Google Sheet"** node
2. Use the same Google Sheets credentials (or create new ones)
3. Set the **Document ID** to your Webinar Registration Sheet ID
4. Set the **Sheet Name** to "Sheet1"
5. Verify the column mappings are correct

#### B. Configure Gmail Node

1. Click on the **"Send Email Notification"** node
2. Use the same Gmail credentials
3. Verify the recipient emails

#### C. Activate the Webhook

1. Click on the **"Webinar Registration Webhook"** node
2. Copy the **Production Webhook URL**
3. The URL will look like: `https://colinryan17.app.n8n.cloud/webhook/webinar`

### Step 6: Save and Activate Workflows

1. Click **Save** in the top right for both workflows
2. Toggle the **Active** switch to ON for both workflows
3. The workflows are now live and ready to receive submissions!

---

## Part 3: Integrate with Your Website

You'll need to update your website forms to POST data to the webhook URLs:

### Contact Form Integration

```javascript
// Example fetch request for contact form
const response = await fetch('https://colinryan17.app.n8n.cloud/webhook/contact', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    first_name: 'John',
    last_name: 'Doe',
    email: 'john@example.com',
    phone: '555-0123',
    message: 'I would like to learn more about your services.',
    submitted_at: new Date().toISOString(),
    source: 'Website Contact Form'
  })
});

const result = await response.json();
console.log(result); // { success: true, message: "Contact form received" }
```

### Webinar Registration Integration

```javascript
// Example fetch request for webinar registration
const response = await fetch('https://colinryan17.app.n8n.cloud/webhook/webinar', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    first_name: 'Jane',
    last_name: 'Smith',
    email: 'jane@example.com',
    agency: 'Department of Defense',
    timeline: '1-2 years',
    submitted_at: new Date().toISOString(),
    source: 'Website Webinar Registration'
  })
});

const result = await response.json();
console.log(result); // { success: true, message: "Webinar registration received" }
```

---

## Testing Your Workflows

### Test Contact Form Workflow

Use this curl command to test:

```bash
curl -X POST https://colinryan17.app.n8n.cloud/webhook/contact \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "phone": "555-0123",
    "message": "This is a test message",
    "submitted_at": "2025-12-17T18:00:00.000Z",
    "source": "Test"
  }'
```

### Test Webinar Registration Workflow

Use this curl command to test:

```bash
curl -X POST https://colinryan17.app.n8n.cloud/webhook/webinar \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "agency": "Department of Test",
    "timeline": "1-2 years",
    "submitted_at": "2025-12-17T18:00:00.000Z",
    "source": "Test"
  }'
```

After testing, check:
1. ✅ Google Sheets - Verify a new row was added
2. ✅ Email - Check that david.fei@planwellfp.com and brennan.rhule@planwellfp.com received the notification
3. ✅ Response - Verify you received `{"success": true, "message": "..."}` response

---

## Troubleshooting

### Issue: "Authentication failed" on Google Sheets

**Solution:**
1. Go to n8n Credentials
2. Delete and recreate the Google Sheets OAuth2 credential
3. Make sure you grant all necessary permissions

### Issue: "Gmail node failed"

**Solution:**
1. Check that Gmail OAuth2 credentials are properly configured
2. Verify the email addresses are correct
3. Make sure the Gmail account has permission to send emails

### Issue: "Webhook not receiving data"

**Solution:**
1. Make sure the workflow is **Active** (toggle is ON)
2. Verify the webhook URL is correct
3. Check that you're sending the correct JSON structure
4. Check n8n's **Executions** tab to see error details

### Issue: "Columns not mapping correctly"

**Solution:**
1. Click on the Google Sheets node
2. Click "Add/Edit Column Mapping"
3. Manually map each field:
   - `First Name` → `={{ $json.first_name }}`
   - `Last Name` → `={{ $json.last_name }}`
   - etc.

---

## Need Help?

- n8n Documentation: https://docs.n8n.io/
- n8n Community: https://community.n8n.io/
- Your n8n Instance: https://colinryan17.app.n8n.cloud/

---

## Summary

✅ **What You Need to Do:**
1. Create 2 Google Sheets with the specified columns
2. Import both JSON workflow files into n8n
3. Configure Google Sheets credentials and Document IDs
4. Configure Gmail credentials
5. Activate both workflows
6. Copy the webhook URLs
7. Integrate webhook URLs into your website forms
8. Test both workflows

**Estimated Setup Time:** 15-20 minutes

Good luck! 🚀
