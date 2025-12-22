"""
Outlook Calendar Integration
============================
Microsoft Graph API integration for checking Outlook calendar availability.

Usage:
    from outlook_calendar import check_availability, get_next_available_slot
    
Environment Variables Required:
    MICROSOFT_CLIENT_ID
    MICROSOFT_CLIENT_SECRET  
    MICROSOFT_TENANT_ID
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

# Microsoft Graph API endpoints
GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"
TOKEN_ENDPOINT = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

# Token cache
_token_cache = {
    'access_token': None,
    'expires_at': None
}


def get_access_token() -> str:
    """
    Get Microsoft Graph API access token using client credentials flow.
    Caches token until expiration.
    """
    global _token_cache
    
    # Check if we have a valid cached token
    if _token_cache['access_token'] and _token_cache['expires_at']:
        if datetime.now() < _token_cache['expires_at']:
            return _token_cache['access_token']
    
    client_id = os.environ.get('MICROSOFT_CLIENT_ID')
    client_secret = os.environ.get('MICROSOFT_CLIENT_SECRET')
    tenant_id = os.environ.get('MICROSOFT_TENANT_ID')
    
    if not all([client_id, client_secret, tenant_id]):
        raise ValueError("Microsoft credentials not configured. Set MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET, and MICROSOFT_TENANT_ID in .env")
    
    token_url = TOKEN_ENDPOINT.format(tenant_id=tenant_id)
    
    response = requests.post(token_url, data={
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    })
    
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.text}")
    
    data = response.json()
    
    # Cache the token
    _token_cache['access_token'] = data['access_token']
    _token_cache['expires_at'] = datetime.now() + timedelta(seconds=data.get('expires_in', 3600) - 60)
    
    return data['access_token']


def check_availability(email: str, start_time: datetime, end_time: datetime) -> dict:
    """
    Check if a user is available during a specific time range.
    
    Args:
        email: User's email address
        start_time: Start of time range to check
        end_time: End of time range to check
        
    Returns:
        Dict with 'available' bool and 'busy_times' list
    """
    access_token = get_access_token()
    
    # Use getSchedule endpoint for availability
    url = f"{GRAPH_API_BASE}/users/{email}/calendar/getSchedule"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'schedules': [email],
        'startTime': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Eastern Standard Time'
        },
        'endTime': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Eastern Standard Time'
        },
        'availabilityViewInterval': 30  # 30-minute slots
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"Calendar check failed for {email}: {response.text}")
        return {'available': True, 'busy_times': [], 'error': response.text}
    
    data = response.json()
    
    if 'value' not in data or len(data['value']) == 0:
        return {'available': True, 'busy_times': []}
    
    schedule = data['value'][0]
    availability_view = schedule.get('availabilityView', '')
    
    # availabilityView is a string where each char represents a 30-min slot
    # 0 = free, 1 = tentative, 2 = busy, 3 = out of office, 4 = working elsewhere
    is_available = all(c == '0' for c in availability_view)
    
    return {
        'available': is_available,
        'availabilityView': availability_view,
        'busy_times': schedule.get('scheduleItems', [])
    }


def get_advisor_availability(advisors: list, check_date: datetime = None) -> dict:
    """
    Check availability for multiple advisors and return a summary.
    
    Args:
        advisors: List of advisor dicts with 'email' field
        check_date: Date to check (defaults to next business day)
        
    Returns:
        Dict mapping advisor email to availability info
    """
    if check_date is None:
        check_date = get_next_business_day()
    
    # Check 9 AM to 5 PM window
    start_time = check_date.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = check_date.replace(hour=17, minute=0, second=0, microsecond=0)
    
    results = {}
    
    for advisor in advisors:
        email = advisor.get('email')
        if email:
            try:
                availability = check_availability(email, start_time, end_time)
                results[email] = availability
            except Exception as e:
                print(f"Error checking availability for {email}: {e}")
                results[email] = {'available': True, 'error': str(e)}
    
    return results


def get_next_business_day() -> datetime:
    """Get the next business day (Monday-Friday)."""
    today = datetime.now()
    days_ahead = 1
    
    next_day = today + timedelta(days=days_ahead)
    
    # If Saturday (5), skip to Monday
    # If Sunday (6), skip to Monday
    while next_day.weekday() >= 5:
        next_day += timedelta(days=1)
    
    return next_day


def select_advisor_by_availability(advisors: list) -> dict:
    """
    Select the best advisor based on availability.
    Falls back to round-robin if both have similar availability.
    
    Args:
        advisors: List of advisor dicts
        
    Returns:
        Selected advisor dict
    """
    availability = get_advisor_availability(advisors)
    
    # Find advisors with availability
    available_advisors = []
    for advisor in advisors:
        email = advisor.get('email')
        if email in availability and availability[email].get('available', False):
            available_advisors.append(advisor)
    
    # If only one is available, return them
    if len(available_advisors) == 1:
        return available_advisors[0]
    
    # If both or neither are available, use round-robin (handled by caller)
    return None


if __name__ == '__main__':
    # Test the calendar integration
    print("Testing Outlook Calendar Integration...")
    
    # This will fail without credentials, but shows the structure
    try:
        token = get_access_token()
        print(f"Got access token: {token[:20]}...")
    except Exception as e:
        print(f"Expected error (credentials not set): {e}")
    
    print("\nTo configure, add to .env:")
    print("MICROSOFT_CLIENT_ID=your_client_id")
    print("MICROSOFT_CLIENT_SECRET=your_client_secret")
    print("MICROSOFT_TENANT_ID=your_tenant_id")
