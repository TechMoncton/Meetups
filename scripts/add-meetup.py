#!/usr/bin/env python3
"""
Add a new meetup entry to the appropriate year's JSON and MD files.

Usage:
  add-meetup.py [--date yyyy-mm-dd] [--time hh:mmam/pm] <topic> <presenter> [<presenter> ...]

Examples:
  add-meetup.py "My crazy topic" "Alex Hart"
  add-meetup.py "My crazy topic" "Alex Hart" "Michael Go"
  add-meetup.py --date 2026-05-01 --time 7:00pm "My crazy topic" "Alex Hart"
"""

import argparse
import json
import os
import re
import sys
from datetime import date, timedelta


def first_friday_of_month(year, month):
    """Return the first Friday of the given month/year.

    >>> first_friday_of_month(2025, 12)  # confirmed by meetup data
    datetime.date(2025, 12, 5)
    >>> first_friday_of_month(2026, 2)
    datetime.date(2026, 2, 6)
    >>> first_friday_of_month(2026, 3)
    datetime.date(2026, 3, 6)
    >>> first_friday_of_month(2027, 1)  # Jan 1 is a Friday in 2027
    datetime.date(2027, 1, 1)
    """
    d = date(year, month, 1)
    days_until_friday = (4 - d.weekday()) % 7  # Friday == weekday 4
    return d + timedelta(days=days_until_friday)


def next_first_friday(today):
    """Return the closest 'first Friday of a month' strictly after today.

    >>> next_first_friday(date(2026, 2, 27))  # day before March's first Friday
    datetime.date(2026, 3, 6)
    >>> next_first_friday(date(2026, 3, 6))   # on the first Friday itself — skip to April
    datetime.date(2026, 4, 3)
    >>> next_first_friday(date(2025, 12, 31)) # after Dec's first Friday — rolls to Jan
    datetime.date(2026, 1, 2)
    >>> next_first_friday(date(2026, 12, 15)) # after Dec's first Friday — rolls to Jan 2027
    datetime.date(2027, 1, 1)
    """
    ff = first_friday_of_month(today.year, today.month)
    if ff > today:
        return ff
    # Current month's first Friday is today or already past — try next month
    next_month = today.month + 1
    next_year = today.year
    if next_month > 12:
        next_month = 1
        next_year += 1
    return first_friday_of_month(next_year, next_month)


def parse_time(time_str):
    """Parse a time string like '6:30pm' or '10:00AM' into '06:30 PM'.

    >>> parse_time("6:30pm")
    '06:30 PM'
    >>> parse_time("6:30PM")
    '06:30 PM'
    >>> parse_time("10:00am")
    '10:00 AM'
    >>> parse_time("12:00pm")
    '12:00 PM'
    >>> parse_time("bad input")
    Traceback (most recent call last):
        ...
    ValueError: Invalid time format: 'bad input'. Expected format like '6:30pm' or '10:00am'.
    """
    time_str = time_str.strip()
    match = re.fullmatch(r'(\d{1,2}):(\d{2})\s*(am|pm)', time_str, re.IGNORECASE)
    if not match:
        raise ValueError(
            f"Invalid time format: '{time_str}'. Expected format like '6:30pm' or '10:00am'."
        )
    hour = int(match.group(1))
    minute = int(match.group(2))
    ampm = match.group(3).upper()
    return f"{hour:02d}:{minute:02d} {ampm}"


def format_date(d):
    """Format a date as 'March 06, 2026'.

    >>> format_date(date(2026, 3, 6))
    'March 06, 2026'
    >>> format_date(date(2025, 12, 5))
    'December 05, 2025'
    """
    return d.strftime("%B %d, %Y")


def get_paths(year):
    """Return (directory, json_path, md_path) for the given year."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    year_dir = os.path.join(repo_root, f"MeetUps {year}")
    json_path = os.path.join(year_dir, f"MeetUps {year}.json")
    md_path = os.path.join(year_dir, f"MeetUps {year}.md")
    return year_dir, json_path, md_path


def update_json(json_path, entry):
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.insert(0, entry)
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def update_md(md_path, entry):
    block = (
        f"Date: {entry['date']}\n"
        f"Time: {entry['time']}\n"
        f"Topic: {entry['topic']}\n"
        f"Presentation: {entry['presentation']}\n"
    )
    if os.path.exists(md_path):
        with open(md_path, "r") as f:
            existing = f.read()
        content = block + "\n" + existing
    else:
        content = block
    with open(md_path, "w") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description="Add a new meetup entry.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--date",
        metavar="yyyy-mm-dd",
        help="Date of the meetup (default: next first Friday of the month)",
    )
    parser.add_argument(
        "--time",
        metavar="hh:mmam/pm",
        default="6:30pm",
        help="Time of the meetup (default: 6:30pm)",
    )
    parser.add_argument("topic", help="Topic of the meetup")
    parser.add_argument("presenters", nargs="+", help="Presenter name(s)")

    args = parser.parse_args()

    # Resolve date
    if args.date:
        try:
            meetup_date = date.fromisoformat(args.date)
        except ValueError:
            print(f"Error: Invalid date '{args.date}'. Expected yyyy-mm-dd.", file=sys.stderr)
            sys.exit(1)
    else:
        meetup_date = next_first_friday(date.today())
        print(f"No date specified. Using next first Friday: {meetup_date}")

    # Parse time
    try:
        time_str = parse_time(args.time)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    year = meetup_date.year
    date_str = format_date(meetup_date)
    presentation_str = ", ".join(args.presenters)

    entry = {
        "date": date_str,
        "time": time_str,
        "topic": args.topic,
        "presentation": presentation_str,
    }

    # Ensure year directory exists
    year_dir, json_path, md_path = get_paths(year)
    os.makedirs(year_dir, exist_ok=True)

    update_json(json_path, entry)
    update_md(md_path, entry)

    print(f"Added meetup entry:")
    print(f"  Date:         {date_str}")
    print(f"  Time:         {time_str}")
    print(f"  Topic:        {args.topic}")
    print(f"  Presentation: {presentation_str}")
    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_path}")


if __name__ == "__main__":
    main()
