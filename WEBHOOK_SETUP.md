# Lead Notification System Setup

## Quick Start - Import n8n Workflows

I've created ready-to-import workflow files. Here's how to set them up:

### Step 1: Import Workflows into n8n

1. Log into your n8n instance: https://colinryan17.app.n8n.cloud
2. Click **"Add workflow"** or the **+** button
3. Click the **three dots menu (⋮)** → **"Import from file"**
4. Import these files from `planwell-site/n8n-workflows/`:
   - `contact-form-workflow.json` - For contact form submissions
   - `webinar-registration-workflow.json` - For webinar registrations

### Step 2: Configure Google Sheets

1. In each workflow, click the **"Add to Google Sheet"** node
2. Click **"Create new credential"** for Google Sheets
3. Follow the OAuth flow to connect your Google account
4. Create a Google Sheet for leads (or use existing)
5. Select the Sheet and add column headers:
   - Contact: First Name, Last Name, Email, Phone, Message, Submitted At, Source
   - Webinar: First Name, Last Name, Email, Agency, Retirement Timeline, Submitted At, Source

### Step 3: Configure Gmail

1. Click the **"Send Email Notification"** node
2. Click **"Create new credential"** for Gmail
3. Authorize with the email account you want to send from
4. Emails will go to: david.fei@planwellfp.com, brennan.rhule@planwellfp.com

### Step 4: Activate & Get Webhook URLs

1. Click **"Save"** on each workflow
2. Toggle the workflow to **Active**
3. Click the **Webhook node** → copy the **Production URL**
4. It will look like: `https://colinryan17.app.n8n.cloud/webhook/contact`

### Step 5: Update Website Forms

Edit these files and replace the webhook URLs:

**Contact Form** (`src/pages/contact.astro`):
```javascript
const CONTACT_WEBHOOK_URL = 'https://colinryan17.app.n8n.cloud/webhook/contact';
```

**Webinar Form** (`src/pages/webinar.astro`):
```javascript
const WEBINAR_WEBHOOK_URL = 'https://colinryan17.app.n8n.cloud/webhook/webinar';
```

---

## What Each Workflow Does

### Contact Form Workflow
1. **Webhook** receives POST from website
2. **Google Sheets** logs the lead
3. **Gmail** sends notification to David & Brennan
4. **Respond** confirms receipt to website

### Webinar Registration Workflow
1. **Webhook** receives POST from website
2. **Google Sheets** logs the registration
3. **Gmail** sends notification to David & Brennan
4. **Respond** confirms receipt to website

---

## Testing

After setup, test by:
1. Go to http://localhost:4321/contact
2. Submit a test form
3. Check your email and Google Sheet for the new entry

---

## Troubleshooting

- **Webhook not responding**: Make sure workflow is Active (toggle is ON)
- **No email received**: Check Gmail credential is authorized
- **Sheet not updating**: Verify Google Sheets credential and sheet selection
