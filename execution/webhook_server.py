"""
Combined Webhook Server
========================
Single Flask server that handles all PlanWell webhooks:
- /api/webinar - Webinar registration (Zoom)
- /api/contact - Contact form (Google Sheets)
- /api/newsletter - Newsletter subscription (Mailchimp)

Run this instead of individual handlers:
    python webhook_server.py
"""

import os
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

app = Flask(__name__)
CORS(app)

# Import and register blueprints/routes from individual handlers
from webinar_nurture_handler import handle_webinar_registration
from contact_form_handler import handle_contact_form
from newsletter_handler import handle_newsletter_subscription

# Re-register routes on the combined app
app.add_url_rule('/api/webinar', 'webinar', handle_webinar_registration, methods=['POST'])
app.add_url_rule('/api/contact', 'contact', handle_contact_form, methods=['POST'])
app.add_url_rule('/api/newsletter', 'newsletter', handle_newsletter_subscription, methods=['POST'])


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return {'status': 'ok', 'service': 'planwell-webhooks'}


# --- Cron Endpoints (called by external cron service like cron-job.org) ---

CRON_SECRET = os.environ.get('CRON_SECRET', 'planwell-cron-2026')


@app.route('/cron/scheduler', methods=['GET', 'POST'])
def cron_scheduler():
    """Run the webinar nurture scheduler. Called hourly by external cron."""
    from flask import request
    if request.args.get('secret') != CRON_SECRET and request.headers.get('X-Cron-Secret') != CRON_SECRET:
        return {'error': 'unauthorized'}, 401
    try:
        from webinar_nurture_scheduler import run_scheduler
        result = run_scheduler()
        return {'status': 'ok', 'result': str(result)}
    except Exception as e:
        print(f"Scheduler cron error: {e}")
        import traceback
        traceback.print_exc()
        return {'status': 'error', 'error': str(e)}, 500


@app.route('/cron/attendance-sync', methods=['GET', 'POST'])
def cron_attendance_sync():
    """Run attendance sync for the latest past webinar. Called daily by external cron."""
    from flask import request
    if request.args.get('secret') != CRON_SECRET and request.headers.get('X-Cron-Secret') != CRON_SECRET:
        return {'error': 'unauthorized'}, 401
    try:
        from zoom_attendance_sync import get_latest_past_webinar, sync_attendance
        webinar = get_latest_past_webinar()
        if not webinar:
            return {'status': 'ok', 'message': 'no past webinar found'}
        result = sync_attendance(webinar['id'], webinar['date_str'], webinar_topic=webinar.get('topic', ''))
        return {'status': 'ok', 'result': result}
    except Exception as e:
        print(f"Attendance sync cron error: {e}")
        import traceback
        traceback.print_exc()
        return {'status': 'error', 'error': str(e)}, 500


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API info."""
    return {
        'service': 'PlanWell Webhook Server',
        'endpoints': [
            {'path': '/api/webinar', 'method': 'POST', 'description': 'Webinar registration'},
            {'path': '/api/contact', 'method': 'POST', 'description': 'Contact form'},
            {'path': '/api/newsletter', 'method': 'POST', 'description': 'Newsletter subscription'},
            {'path': '/health', 'method': 'GET', 'description': 'Health check'},
            {'path': '/cron/scheduler', 'method': 'GET', 'description': 'Run email scheduler (requires secret)'},
            {'path': '/cron/attendance-sync', 'method': 'GET', 'description': 'Run attendance sync (requires secret)'},
        ]
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"\n{'='*60}")
    print(f"PlanWell Webhook Server")
    print(f"{'='*60}")
    print(f"Running on http://localhost:{port}")
    print(f"\nEndpoints:")
    print(f"  POST /api/webinar     - Webinar registration")
    print(f"  POST /api/contact     - Contact form")
    print(f"  POST /api/newsletter  - Newsletter subscription")
    print(f"  GET  /health          - Health check")
    print(f"{'='*60}\n")
    app.run(host='0.0.0.0', port=port, debug=True)
