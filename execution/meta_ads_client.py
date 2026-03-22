"""
Meta Marketing API Client
==========================
Manages ad campaigns for PlanWell webinar registration via Meta Ads.

API Docs: https://developers.facebook.com/docs/marketing-apis
Auth: Bearer token (long-lived access token)
API Version: v20.0

All campaigns are created as PAUSED by default (semi-automated workflow).
Colin reviews in Ads Manager and clicks Publish.
"""

import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / '.env')

META_APP_ID = os.environ.get('META_APP_ID', '')
META_APP_SECRET = os.environ.get('META_APP_SECRET', '')
META_ACCESS_TOKEN = os.environ.get('META_ACCESS_TOKEN', '')
META_AD_ACCOUNT_ID = os.environ.get('META_AD_ACCOUNT_ID', '')
META_PIXEL_ID = os.environ.get('META_PIXEL_ID', '')
META_PAGE_ID = os.environ.get('META_PAGE_ID', '')

BASE_URL = 'https://graph.facebook.com/v20.0'


def _headers():
    return {
        'Authorization': f'Bearer {META_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }


def create_campaign(name, objective='OUTCOME_TRAFFIC', budget_cents=2000, status='PAUSED'):
    """
    Create a new ad campaign.

    Args:
        name: Campaign name (e.g., 'FERS Webinar - Mar 2026')
        objective: Campaign objective (OUTCOME_TRAFFIC, OUTCOME_LEADS, etc.)
        budget_cents: Daily budget in cents (default $20.00)
        status: Campaign status (PAUSED or ACTIVE)

    Returns:
        dict with success status and campaign_id
    """
    url = f'{BASE_URL}/act_{META_AD_ACCOUNT_ID}/campaigns'

    payload = {
        'name': name,
        'objective': objective,
        'status': status,
        'special_ad_categories': [],
        'daily_budget': budget_cents,
    }

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=15)

        if resp.status_code == 200:
            campaign_id = resp.json().get('id')
            print(f"Campaign created: {campaign_id} ({name})")
            return {'success': True, 'campaign_id': campaign_id}
        else:
            print(f'Meta API error: {resp.status_code} - {resp.text}')
            return {'success': False, 'error': resp.text, 'status_code': resp.status_code}

    except Exception as e:
        print(f'Meta API request failed: {e}')
        return {'success': False, 'error': str(e)}


def create_ad_set(campaign_id, name, targeting, daily_budget_cents, start_time, end_time):
    """
    Create an ad set within a campaign.

    Args:
        campaign_id: Parent campaign ID
        name: Ad set name
        targeting: Targeting dict (use build_targeting() helper)
        daily_budget_cents: Daily budget in cents
        start_time: ISO 8601 start time
        end_time: ISO 8601 end time

    Returns:
        dict with success status and ad_set_id
    """
    url = f'{BASE_URL}/act_{META_AD_ACCOUNT_ID}/adsets'

    payload = {
        'name': name,
        'campaign_id': campaign_id,
        'daily_budget': daily_budget_cents,
        'billing_event': 'IMPRESSIONS',
        'optimization_goal': 'LINK_CLICKS',
        'targeting': targeting,
        'start_time': start_time,
        'end_time': end_time,
        'status': 'PAUSED',
    }

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=15)

        if resp.status_code == 200:
            ad_set_id = resp.json().get('id')
            print(f"Ad set created: {ad_set_id} ({name})")
            return {'success': True, 'ad_set_id': ad_set_id}
        else:
            print(f'Meta API error: {resp.status_code} - {resp.text}')
            return {'success': False, 'error': resp.text, 'status_code': resp.status_code}

    except Exception as e:
        print(f'Meta API request failed: {e}')
        return {'success': False, 'error': str(e)}


def create_ad(ad_set_id, name, creative_id, copy_text, headline, link_url, cta_type='LEARN_MORE'):
    """
    Create an ad within an ad set.

    Args:
        ad_set_id: Parent ad set ID
        name: Ad name
        creative_id: Ad creative ID (from create_ad_creative)
        copy_text: Primary text (body copy)
        headline: Headline text
        link_url: Destination URL
        cta_type: Call-to-action type (LEARN_MORE, SIGN_UP, etc.)

    Returns:
        dict with success status and ad_id
    """
    url = f'{BASE_URL}/act_{META_AD_ACCOUNT_ID}/ads'

    payload = {
        'name': name,
        'adset_id': ad_set_id,
        'creative': {'creative_id': creative_id},
        'status': 'PAUSED',
    }

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=15)

        if resp.status_code == 200:
            ad_id = resp.json().get('id')
            print(f"Ad created: {ad_id} ({name})")
            return {'success': True, 'ad_id': ad_id}
        else:
            print(f'Meta API error: {resp.status_code} - {resp.text}')
            return {'success': False, 'error': resp.text, 'status_code': resp.status_code}

    except Exception as e:
        print(f'Meta API request failed: {e}')
        return {'success': False, 'error': str(e)}


def upload_image(image_path):
    """
    Upload an image to the ad account for use in creatives.

    Args:
        image_path: Local path to image file

    Returns:
        dict with success status and image_hash
    """
    url = f'{BASE_URL}/act_{META_AD_ACCOUNT_ID}/adimages'

    try:
        with open(image_path, 'rb') as img_file:
            files = {'filename': img_file}
            headers = {'Authorization': f'Bearer {META_ACCESS_TOKEN}'}
            resp = requests.post(url, files=files, headers=headers, timeout=30)

        if resp.status_code == 200:
            images = resp.json().get('images', {})
            # Response is keyed by filename
            for key, val in images.items():
                image_hash = val.get('hash')
                print(f"Image uploaded: {image_hash}")
                return {'success': True, 'image_hash': image_hash}
            return {'success': False, 'error': 'No image hash in response'}
        else:
            print(f'Meta API error: {resp.status_code} - {resp.text}')
            return {'success': False, 'error': resp.text, 'status_code': resp.status_code}

    except Exception as e:
        print(f'Meta API request failed: {e}')
        return {'success': False, 'error': str(e)}


def create_ad_creative(name, image_hash, body, title, link_url, cta_type='LEARN_MORE'):
    """
    Create an ad creative (image + copy combination).

    Args:
        name: Creative name
        image_hash: Image hash from upload_image()
        body: Primary text (main copy)
        title: Headline text
        link_url: Destination URL
        cta_type: Call-to-action type

    Returns:
        dict with success status and creative_id
    """
    url = f'{BASE_URL}/act_{META_AD_ACCOUNT_ID}/adcreatives'

    payload = {
        'name': name,
        'object_story_spec': {
            'page_id': META_PAGE_ID,
            'link_data': {
                'image_hash': image_hash,
                'link': link_url,
                'message': body,
                'name': title,
                'call_to_action': {
                    'type': cta_type,
                    'value': {'link': link_url},
                },
            },
        },
    }

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=15)

        if resp.status_code == 200:
            creative_id = resp.json().get('id')
            print(f"Creative created: {creative_id} ({name})")
            return {'success': True, 'creative_id': creative_id}
        else:
            print(f'Meta API error: {resp.status_code} - {resp.text}')
            return {'success': False, 'error': resp.text, 'status_code': resp.status_code}

    except Exception as e:
        print(f'Meta API request failed: {e}')
        return {'success': False, 'error': str(e)}


def get_campaign_insights(campaign_id, date_preset='last_7d'):
    """
    Get performance insights for a campaign.

    Args:
        campaign_id: Campaign ID to get insights for
        date_preset: Date range (last_7d, last_30d, today, yesterday, etc.)

    Returns:
        dict with impressions, clicks, ctr, spend, actions
    """
    url = f'{BASE_URL}/{campaign_id}/insights'

    params = {
        'date_preset': date_preset,
        'fields': 'impressions,clicks,ctr,spend,actions,cost_per_action_type,reach,frequency',
    }

    try:
        resp = requests.get(url, params=params, headers=_headers(), timeout=15)

        if resp.status_code == 200:
            data = resp.json().get('data', [])
            if data:
                insight = data[0]
                return {
                    'impressions': int(insight.get('impressions', 0)),
                    'clicks': int(insight.get('clicks', 0)),
                    'ctr': float(insight.get('ctr', 0)),
                    'spend': float(insight.get('spend', 0)),
                    'reach': int(insight.get('reach', 0)),
                    'frequency': float(insight.get('frequency', 0)),
                    'actions': insight.get('actions', []),
                    'cost_per_action': insight.get('cost_per_action_type', []),
                }
            return {'impressions': 0, 'clicks': 0, 'ctr': 0, 'spend': 0}
        else:
            print(f'Meta API error: {resp.status_code} - {resp.text}')
            return {'error': resp.text, 'status_code': resp.status_code}

    except Exception as e:
        print(f'Meta API request failed: {e}')
        return {'error': str(e)}


def list_campaigns(status_filter=None):
    """
    List all campaigns in the ad account.

    Args:
        status_filter: Optional status filter ('ACTIVE', 'PAUSED', 'ARCHIVED')

    Returns:
        list of campaign dicts with id, name, status, daily_budget
    """
    url = f'{BASE_URL}/act_{META_AD_ACCOUNT_ID}/campaigns'

    params = {
        'fields': 'id,name,status,daily_budget,objective,created_time',
        'limit': 50,
    }
    if status_filter:
        params['effective_status'] = [status_filter]

    try:
        resp = requests.get(url, params=params, headers=_headers(), timeout=15)

        if resp.status_code == 200:
            campaigns = []
            for c in resp.json().get('data', []):
                campaigns.append({
                    'id': c.get('id'),
                    'name': c.get('name'),
                    'status': c.get('status'),
                    'daily_budget': c.get('daily_budget'),
                    'objective': c.get('objective'),
                    'created_time': c.get('created_time'),
                })
            return campaigns
        else:
            print(f'Meta API error: {resp.status_code} - {resp.text}')
            return []

    except Exception as e:
        print(f'Meta API request failed: {e}')
        return []


def pause_campaign(campaign_id):
    """
    Pause an active campaign.

    Args:
        campaign_id: Campaign ID to pause

    Returns:
        bool indicating success
    """
    url = f'{BASE_URL}/{campaign_id}'
    payload = {'status': 'PAUSED'}

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=15)
        if resp.status_code == 200:
            print(f"Campaign {campaign_id} paused")
            return True
        else:
            print(f'Meta API error: {resp.status_code} - {resp.text}')
            return False

    except Exception as e:
        print(f'Meta API request failed: {e}')
        return False


def resume_campaign(campaign_id):
    """
    Resume a paused campaign.

    Args:
        campaign_id: Campaign ID to resume

    Returns:
        bool indicating success
    """
    url = f'{BASE_URL}/{campaign_id}'
    payload = {'status': 'ACTIVE'}

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=15)
        if resp.status_code == 200:
            print(f"Campaign {campaign_id} resumed")
            return True
        else:
            print(f'Meta API error: {resp.status_code} - {resp.text}')
            return False

    except Exception as e:
        print(f'Meta API request failed: {e}')
        return False


def get_ad_library_ads(search_terms, country='US'):
    """
    Search the Meta Ad Library for competitor ads.

    Args:
        search_terms: Keywords to search for
        country: Country code (default US)

    Returns:
        list of ad dicts with page_name, body_text, link_url, status
    """
    url = f'{BASE_URL}/ads_archive'

    params = {
        'search_terms': search_terms,
        'ad_reached_countries': [country],
        'ad_type': 'ALL',
        'fields': 'page_name,ad_creative_bodies,ad_creative_link_titles,ad_creative_link_captions,ad_delivery_start_time,ad_delivery_stop_time',
        'limit': 25,
        'access_token': META_ACCESS_TOKEN,
    }

    try:
        resp = requests.get(url, params=params, timeout=15)

        if resp.status_code == 200:
            ads = []
            for ad in resp.json().get('data', []):
                ads.append({
                    'page_name': ad.get('page_name', ''),
                    'body_text': (ad.get('ad_creative_bodies') or [''])[0],
                    'headline': (ad.get('ad_creative_link_titles') or [''])[0],
                    'start_date': ad.get('ad_delivery_start_time', ''),
                    'end_date': ad.get('ad_delivery_stop_time', ''),
                })
            return ads
        else:
            print(f'Ad Library API error: {resp.status_code} - {resp.text}')
            return []

    except Exception as e:
        print(f'Ad Library request failed: {e}')
        return []


def build_targeting(age_min=40, age_max=62, interests=None, custom_audiences=None, lookalike_source=None):
    """
    Build a targeting dict for ad sets.

    Args:
        age_min: Minimum age (default 40 for federal retirement audience)
        age_max: Maximum age (default 62)
        interests: List of interest dicts [{'id': '...', 'name': '...'}]
        custom_audiences: List of custom audience IDs
        lookalike_source: Source audience ID for lookalike creation

    Returns:
        dict formatted for Meta targeting API
    """
    targeting = {
        'age_min': age_min,
        'age_max': age_max,
        'geo_locations': {
            'countries': ['US'],
        },
    }

    if interests:
        targeting['flexible_spec'] = [{'interests': interests}]

    if custom_audiences:
        targeting['custom_audiences'] = [{'id': ca_id} for ca_id in custom_audiences]

    if lookalike_source:
        targeting['custom_audiences'] = targeting.get('custom_audiences', [])
        targeting['custom_audiences'].append({'id': lookalike_source})

    return targeting


# Common interest targets for federal employee webinars
FEDERAL_EMPLOYEE_INTERESTS = [
    {'id': '6003139266461', 'name': 'Federal government of the United States'},
    {'id': '6003384248805', 'name': 'Retirement planning'},
    {'id': '6003020834693', 'name': 'Government employee'},
]


if __name__ == '__main__':
    """Test: list campaigns and check API connectivity."""
    import sys

    if '--campaigns' in sys.argv:
        print("Active Campaigns:")
        print("-" * 40)
        campaigns = list_campaigns(status_filter='ACTIVE')
        if campaigns:
            for c in campaigns:
                print(f"  {c['name']} (ID: {c['id']}, Budget: ${int(c.get('daily_budget', 0))/100:.2f}/day)")
        else:
            print("  No active campaigns found.")

        print()
        print("Paused Campaigns:")
        print("-" * 40)
        paused = list_campaigns(status_filter='PAUSED')
        if paused:
            for c in paused:
                print(f"  {c['name']} (ID: {c['id']})")
        else:
            print("  No paused campaigns.")

    elif '--spy' in sys.argv:
        query = ' '.join(sys.argv[sys.argv.index('--spy')+1:]) or 'federal retirement planning'
        print(f"Ad Library search: '{query}'")
        print("-" * 40)
        ads = get_ad_library_ads(query)
        for ad in ads[:10]:
            print(f"  Page: {ad['page_name']}")
            print(f"  Copy: {ad['body_text'][:100]}...")
            print(f"  Started: {ad['start_date']}")
            print()

    else:
        print("Meta Ads Client")
        print("-" * 40)
        campaigns = list_campaigns()
        print(f"Total campaigns: {len(campaigns)}")
        for c in campaigns[:5]:
            print(f"  {c['name']} [{c['status']}]")
        print()
        print("Tip: Use --campaigns for active/paused breakdown, --spy <query> for Ad Library search.")
