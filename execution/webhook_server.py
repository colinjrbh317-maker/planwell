"""
Combined Webhook Server
========================
Single Flask server that handles all PlanWell webhooks:
- /api/webinar - Webinar registration
- /api/contact - Contact form
- /api/book-call - Call booking

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

# Re-register routes on the combined app
app.add_url_rule('/api/webinar', 'webinar', handle_webinar_registration, methods=['POST'])
app.add_url_rule('/api/contact', 'contact', handle_contact_form, methods=['POST'])


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return {'status': 'ok', 'service': 'planwell-webhooks'}


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API info."""
    return {
        'service': 'PlanWell Webhook Server',
        'endpoints': [
            {'path': '/api/webinar', 'method': 'POST', 'description': 'Webinar registration'},
            {'path': '/api/contact', 'method': 'POST', 'description': 'Contact form'},
            {'path': '/health', 'method': 'GET', 'description': 'Health check'},
        ]
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"\n{'='*60}")
    print(f"PlanWell Webhook Server")
    print(f"{'='*60}")
    print(f"Running on http://localhost:{port}")
    print(f"\nEndpoints:")
    print(f"  POST /api/webinar  - Webinar registration")
    print(f"  POST /api/contact  - Contact form")
    print(f"  GET  /health       - Health check")
    print(f"{'='*60}\n")
    app.run(host='0.0.0.0', port=port, debug=True)
