"""
Newsletter Subscription Handler
================================
Receives newsletter subscriptions from the homepage popup
and adds subscribers to Mailchimp. The Mailchimp customer journey
auto-sends the free FERS guide email.

Endpoint: POST /api/newsletter
Payload: { name, email, source, timestamp }
"""

from flask import request, jsonify
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from mailchimp_client import add_subscriber as mailchimp_add_subscriber


def handle_newsletter_subscription():
    """
    Handle newsletter subscription from homepage popup.
    Adds subscriber to Mailchimp with 'free-guide' tag.
    Mailchimp customer journey auto-sends the FERS guide.

    Expected payload:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "source": "homepage_popup",
        "timestamp": "2024-01-15T10:30:00.000Z"
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data or 'email' not in data:
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400

        name = data.get('name', '')
        email = data['email'].strip().lower()
        source = data.get('source', 'homepage_popup')

        # Add to Mailchimp (tags trigger customer journey for free guide)
        mc_result = mailchimp_add_subscriber(
            email=email,
            first_name=name.split()[0] if name else '',
            tags=['free-guide', source]
        )

        if mc_result.get('success'):
            print(f"Newsletter subscription: {email} -> Mailchimp {mc_result.get('status', 'subscribed')}")
        else:
            print(f"Mailchimp error for {email}: {mc_result.get('error', 'unknown')}")

        return jsonify({
            'success': mc_result.get('success', False),
            'message': 'Subscribed successfully' if mc_result.get('success') else 'Subscription failed',
            'mailchimp': mc_result.get('status', 'unknown'),
            'duplicate': mc_result.get('duplicate', False)
        })

    except Exception as e:
        print(f"Error processing newsletter subscription: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    """Test the handler locally."""
    from flask import Flask
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app)

    app.add_url_rule('/api/newsletter', 'newsletter', handle_newsletter_subscription, methods=['POST'])

    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'ok', 'service': 'newsletter-handler'}

    port = int(os.environ.get('PORT', 5002))
    print(f"\nNewsletter Handler running on http://localhost:{port}")
    print(f"POST /api/newsletter - Newsletter subscription")
    app.run(host='0.0.0.0', port=port, debug=True)
