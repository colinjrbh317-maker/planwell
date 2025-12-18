# ✅ Google Sheets Created! Next Steps for n8n

Your Google Sheets have been created successfully! Now you need to configure your n8n workflows.

---

## 📊 Your Sheet IDs

### Contact Form Sheet
- **Sheet ID:** `1PPlKtkjrIrlev5U5QuaKuocwNMbFqj2TLHdSwv1BDYo`
- **URL:** https://docs.google.com/spreadsheets/d/1PPlKtkjrIrlev5U5QuaKuocwNMbFqj2TLHdSwv1BDYo/edit

### Webinar Registration Sheet
- **Sheet ID:** `1hfZaFYNwdAW6GC78HkQpCBf6yWqH-AqUZwVtTGgA4bo`
- **URL:** https://docs.google.com/spreadsheets/d/1hfZaFYNwdAW6GC78HkQpCBf6yWqH-AqUZwVtTGgA4bo/edit

---

## 🔧 Configure n8n Workflows

### Workflow 1: Contact Form Notifications

1. Go to https://colinryan17.app.n8n.cloud/
2. Open the **"PlanWell Contact Form Notifications"** workflow
3. Click the **"Add to Google Sheet"** node

#### Configure Google Sheets:
```
1. Click "Credential for Google Sheets"
2. Click "Create New Credential"
3. Click "Sign in with Google"
4. Choose your Google account
5. Grant permissions (allow access to Google Sheets)
```

#### Set Document ID:
```
Document ID: 1PPlKtkjrIrlev5U5QuaKuocwNMbFqj2TLHdSwv1BDYo
Sheet Name: Sheet1
```

4. Click the **"Send Email Notification"** node

#### Configure Gmail:
```
1. Click "Credential for Gmail"
2. Click "Create New Credential"
3. Click "Sign in with Google"
4. Choose your Gmail account
5. Grant permissions (allow sending emails)
```

#### Verify Recipients:
```
Recipients: david.fei@planwellfp.com, brennan.rhule@planwellfp.com
```

5. **Save** the workflow (click Save button)
6. **Activate** the workflow (toggle switch to ON - it should turn green)
7. **Copy the webhook URL** from the "Contact Form Webhook" node
   - Should be: `https://colinryan17.app.n8n.cloud/webhook/contact`

---

### Workflow 2: Webinar Registration Notifications

1. Open the **"PlanWell Webinar Registration Notifications"** workflow
2. Click the **"Add to Google Sheet"** node

#### Set Document ID:
```
Credential: Use the same Google Sheets credential from Workflow 1
Document ID: 1hfZaFYNwdAW6GC78HkQpCBf6yWqH-AqUZwVtTGgA4bo
Sheet Name: Sheet1
```

3. Click the **"Send Email Notification"** node

#### Configure Gmail:
```
Credential: Use the same Gmail credential from Workflow 1
Recipients: david.fei@planwellfp.com, brennan.rhule@planwellfp.com
```

4. **Save** the workflow
5. **Activate** the workflow (toggle ON)
6. **Copy the webhook URL** from the "Webinar Registration Webhook" node
   - Should be: `https://colinryan17.app.n8n.cloud/webhook/webinar`

---

## 🧪 Test Your Workflows

### Test Contact Form:

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

**Expected response:**
```json
{"success": true, "message": "Contact form received"}
```

### Test Webinar Registration:

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

**Expected response:**
```json
{"success": true, "message": "Webinar registration received"}
```

---

## ✅ Verification Checklist

After testing, verify:

- [ ] New row appears in Google Sheets (Contact Form)
- [ ] New row appears in Google Sheets (Webinar)
- [ ] Email received by david.fei@planwellfp.com
- [ ] Email received by brennan.rhule@planwellfp.com
- [ ] JSON response received: `{"success": true, "message": "..."}`

---

## 📱 Use in Your Website

Once tested and verified, use these webhook URLs in your website forms:

### Contact Form:
```javascript
const response = await fetch('https://colinryan17.app.n8n.cloud/webhook/contact', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    first_name: formData.firstName,
    last_name: formData.lastName,
    email: formData.email,
    phone: formData.phone,
    message: formData.message,
    submitted_at: new Date().toISOString(),
    source: 'Website Contact Form'
  })
});
```

### Webinar Registration:
```javascript
const response = await fetch('https://colinryan17.app.n8n.cloud/webhook/webinar', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    first_name: formData.firstName,
    last_name: formData.lastName,
    email: formData.email,
    agency: formData.agency,
    timeline: formData.timeline,
    submitted_at: new Date().toISOString(),
    source: 'Website Webinar Registration'
  })
});
```

---

## 🎉 You're Done!

Your n8n workflows are now ready to:
- ✅ Receive form submissions from your website
- ✅ Save them to Google Sheets
- ✅ Send email notifications
- ✅ Return success responses

---

**Need help?** Check the other documentation files or the n8n Executions tab to debug any issues.
