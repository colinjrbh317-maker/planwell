"""
GReminders Calendar Integration
Simple calendar availability checking using local storage
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class GRemindersCalendar:
    """Simple calendar management for David and Brennan"""
    
    def __init__(self):
        self.calendar_file = os.path.join(os.path.dirname(__file__), 'calendar_bookings.json')
        self._ensure_calendar_file()
    
    def _ensure_calendar_file(self):
        """Create calendar file if it doesn't exist"""
        if not os.path.exists(self.calendar_file):
            with open(self.calendar_file, 'w') as f:
                json.dump({
                    'david.fei@planwellfp.com': [],
                    'brennan.rhule@planwellfp.com': []
                }, f, indent=2)
    
    def _load_calendar(self) -> Dict:
        """Load calendar from file"""
        with open(self.calendar_file, 'r') as f:
            return json.load(f)
    
    def _save_calendar(self, calendar: Dict):
        """Save calendar to file"""
        with open(self.calendar_file, 'w') as f:
            json.dump(calendar, f, indent=2)
    
    def check_availability(self, email: str, start_time: datetime, duration_minutes: int = 60) -> bool:
        """
        Check if advisor is available at the given time
        
        Args:
            email: Advisor email (david.fei@planwellfp.com or brennan.rhule@planwellfp.com)
            start_time: Proposed meeting start time
            duration_minutes: Meeting duration in minutes
            
        Returns:
            True if available, False if busy
        """
        calendar = self._load_calendar()
        
        if email not in calendar:
            return False
        
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        # Check existing bookings for conflicts
        for booking in calendar[email]:
            booking_start = datetime.fromisoformat(booking['start_time'])
            booking_end = datetime.fromisoformat(booking['end_time'])
            
            # Check if times overlap
            if (start_time < booking_end and end_time > booking_start):
                return False  # Conflict found
        
        return True  # No conflicts
    
    def create_booking(
        self, 
        email: str, 
        start_time: datetime, 
        duration_minutes: int,
        client_name: str,
        client_email: str,
        client_phone: str,
        notes: str = ""
    ) -> Dict:
        """
        Create a new booking
        
        Returns:
            Booking details dictionary
        """
        calendar = self._load_calendar()
        
        booking = {
            'id': f"{int(start_time.timestamp())}_{email.split('@')[0]}",
            'start_time': start_time.isoformat(),
            'end_time': (start_time + timedelta(minutes=duration_minutes)).isoformat(),
            'client_name': client_name,
            'client_email': client_email,
            'client_phone': client_phone,
            'notes': notes,
            'created_at': datetime.now().isoformat()
        }
        
        calendar[email].append(booking)
        self._save_calendar(calendar)
        
        return booking
    
    def get_bookings(
        self, 
        email: str, 
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> List[Dict]:
        """Get bookings for an advisor within a date range"""
        calendar = self._load_calendar()
        
        if email not in calendar:
            return []
        
        bookings = calendar[email]
        
        # Filter by date range if provided
        if from_date or to_date:
            filtered = []
            for booking in bookings:
                booking_start = datetime.fromisoformat(booking['start_time'])
                
                if from_date and booking_start < from_date:
                    continue
                if to_date and booking_start > to_date:
                    continue
                    
                filtered.append(booking)
            return filtered
        
        return bookings
    
    def find_next_available_slot(
        self,
        email: str,
        preferred_date: datetime,
        duration_minutes: int = 60,
        business_hours_start: int = 9,  # 9 AM
        business_hours_end: int = 17,    # 5 PM
        search_days: int = 14
    ) -> Optional[datetime]:
        """
        Find the next available time slot for an advisor
        
        Args:
            email: Advisor email
            preferred_date: Start searching from this date
            duration_minutes: Meeting duration
            business_hours_start: Start of business day (hour)
            business_hours_end: End of business day (hour)
            search_days: Number of days to search ahead
            
        Returns:
            Next available datetime or None
        """
        current_date = preferred_date.replace(hour=business_hours_start, minute=0, second=0, microsecond=0)
        end_search = current_date + timedelta(days=search_days)
        
        while current_date < end_search:
            # Skip weekends
            if current_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
                current_date += timedelta(days=1)
                current_date = current_date.replace(hour=business_hours_start, minute=0)
                continue
            
            # Check hourly slots
            for hour in range(business_hours_start, business_hours_end):
                slot_time = current_date.replace(hour=hour, minute=0)
                
                if self.check_availability(email, slot_time, duration_minutes):
                    return slot_time
            
            # Move to next day
            current_date += timedelta(days=1)
            current_date = current_date.replace(hour=business_hours_start, minute=0)
        
        return None  # No availability found


# Singleton instance
_calendar = None

def get_calendar() -> GRemindersCalendar:
    """Get the calendar singleton instance"""
    global _calendar
    if _calendar is None:
        _calendar = GRemindersCalendar()
    return _calendar
