"""
Date and time types in Python.
"""
from datetime import datetime, date, time, timedelta, timezone
import calendar

# Current date and time
now = datetime.now()
utc_now = datetime.now(timezone.utc)
print(f"Now: {now}")
print(f"UTC Now: {utc_now}")

# Creating dates
d = date(2024, 3, 15)
t = time(14, 30, 45)
dt = datetime(2024, 3, 15, 14, 30, 45)
print(f"Date: {d}, Time: {t}, DateTime: {dt}")

# Parsing strings
parsed = datetime.strptime("2024-03-15 14:30:00", "%Y-%m-%d %H:%M:%S")
print(f"Parsed: {parsed}")

# Formatting
formatted = now.strftime("%B %d, %Y at %I:%M %p")
print(f"Formatted: {formatted}")

# ISO format
iso = now.isoformat()
print(f"ISO format: {iso}")
from_iso = datetime.fromisoformat(iso)
print(f"From ISO: {from_iso}")

# Timedelta
tomorrow = now + timedelta(days=1)
last_week = now - timedelta(weeks=1)
print(f"Tomorrow: {tomorrow.date()}")
print(f"Last week: {last_week.date()}")

# Difference between dates
birthday = date(1990, 6, 15)
age_days = (date.today() - birthday).days
print(f"Age in days: {age_days}")
print(f"Age in years: {age_days // 365}")

# Timezone handling
eastern = timezone(timedelta(hours=-5))
pacific = timezone(timedelta(hours=-8))
now_eastern = datetime.now(eastern)
now_pacific = now_eastern.astimezone(pacific)
print(f"Eastern: {now_eastern}")
print(f"Pacific: {now_pacific}")

# Calendar
print(f"\nCalendar March 2024:")
print(calendar.month(2024, 3))
print(f"Is 2024 a leap year? {calendar.isleap(2024)}")

# Date components
print(f"Year: {now.year}, Month: {now.month}, Day: {now.day}")
print(f"Hour: {now.hour}, Minute: {now.minute}, Second: {now.second}")
print(f"Weekday: {now.strftime('%A')}")
print(f"Day of year: {now.timetuple().tm_yday}")
