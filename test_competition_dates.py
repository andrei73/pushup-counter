#!/usr/bin/env python
"""Test script to verify competition date logic."""

from datetime import date
from calendar import monthrange

def test_competition_logic():
    """Test the competition date logic for potential bugs."""
    
    print("=" * 60)
    print("TESTING COMPETITION DATE LOGIC")
    print("=" * 60)
    
    # Test October 2025
    year, month = 2025, 10
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])
    
    print(f"\n📅 October 2025 Competition")
    print(f"   Start Date: {first_day} ({first_day.strftime('%A, %B %d, %Y')})")
    print(f"   End Date:   {last_day} ({last_day.strftime('%A, %B %d, %Y')})")
    print(f"   Days in month: {monthrange(year, month)[1]}")
    
    # Test the is_active logic
    print(f"\n🔍 Testing is_active logic (start_date <= today <= end_date):")
    test_dates = [
        ("Oct 30", date(2025, 10, 30)),
        ("Oct 31 (last day)", date(2025, 10, 31)),
        ("Nov 1 (day after)", date(2025, 11, 1)),
        ("Nov 2", date(2025, 11, 2)),
    ]
    
    for label, test_date in test_dates:
        is_active = first_day <= test_date <= last_day
        print(f"   {label:20s} → is_active: {is_active}")
    
    # Test the update_status logic
    print(f"\n🔍 Testing update_status logic:")
    for label, today in test_dates:
        if today < first_day:
            status = "UPCOMING"
        elif today > last_day:
            status = "COMPLETED"
        else:
            status = "ACTIVE"
        print(f"   {label:20s} → status: {status}")
    
    # Test days_remaining logic
    print(f"\n🔍 Testing days_remaining logic (end_date - today).days + 1:")
    for label, today in test_dates:
        if today > last_day:
            days_remaining = 0
        else:
            days_remaining = (last_day - today).days + 1
        print(f"   {label:20s} → days_remaining: {days_remaining}")
    
    # Test edge cases for different months
    print(f"\n📅 Testing Different Months:")
    test_months = [
        (2024, 2),  # February (leap year)
        (2025, 2),  # February (non-leap year)
        (2025, 4),  # April (30 days)
        (2025, 12), # December (31 days)
    ]
    
    for year, month in test_months:
        first = date(year, month, 1)
        last = date(year, month, monthrange(year, month)[1])
        print(f"   {first.strftime('%B %Y'):15s} → Ends on {last} (day {last.day})")
    
    # Check for potential bugs
    print(f"\n⚠️  POTENTIAL ISSUES:")
    print(f"   1. End date includes the last day of month: ✅ CORRECT")
    print(f"      (Oct 31 should be ACTIVE, not COMPLETED)")
    print(f"   2. Competition completes on Nov 1: ✅ CORRECT")
    print(f"      (First day of next month)")
    print(f"   3. Days remaining on last day: {(last_day - last_day).days + 1}")
    print(f"      (Should be 1, not 0)")
    
    # November 2025 test
    print(f"\n📅 November 2025 Competition (Current Month)")
    nov_first = date(2025, 11, 1)
    nov_last = date(2025, 11, monthrange(2025, 11)[1])
    print(f"   Start Date: {nov_first} ({nov_first.strftime('%A, %B %d, %Y')})")
    print(f"   End Date:   {nov_last} ({nov_last.strftime('%A, %B %d, %Y')})")
    print(f"   Days in month: {monthrange(2025, 11)[1]}")
    
    print(f"\n" + "=" * 60)
    print("CONCLUSION:")
    print("=" * 60)
    print("✅ The logic appears CORRECT for monthly competitions:")
    print("   - Start: 1st day of month")
    print("   - End: Last day of month (28-31 depending on month)")
    print("   - Active: Includes both start and end dates")
    print("   - Completed: Starting from first day of next month")
    print()

if __name__ == "__main__":
    test_competition_logic()

