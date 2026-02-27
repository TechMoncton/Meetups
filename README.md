# Tech Moncton

A friendly, inclusive meetup for Moncton’s tech and developer community to connect, share ideas, and build local relationships.

---

## When and Where
- **Regular meeting time**: First Friday of every month unless stated otherwise.  
- **Start time**: 6:30 PM.  
- **Venue**: [Venn Innovation, 770 St. George Boulevard](https://www.google.ca/maps/place/Venn+Innovation/@46.0843704,-64.8116575,17z/data=!3m1!4b1!4m6!3m5!1s0x4ca0b9396aa0ce8d:0x2ab3f8a8d17c244a!8m2!3d46.0843704!4d-64.8116575!16s%2Fg%2F11cry099th).  
- **After meetup**: There is typically a meal and drinks at a nearby restaurant or pub after the meeting.

## Discord Hub
**Join our main place to chat and hang out between meetups**  
**Discord Invite**: [https://discord.gg/axYagWhk6Y](https://discord.gg/axYagWhk6Y)

- **Primary community space** for announcements, casual conversation, event planning, and followups from talks.
- Use the Discord to ask questions, share job posts, show projects, find collaborators, and organize ad hoc meetups.
- New members are welcome to introduce themselves and jump into any topic channel.

---

## What to Expect
- **No fees**: No formal membership or dues required.
- **Format**: Short talks, lightning demos, show-and-tell, or open discussions led by local members.  
- **Tone**: Casual, helpful, and community focused. Sessions are designed to be accessible to a range of experience levels.  
- **Networking**: Time to meet others working on similar technologies or projects, plus the social portion after the meeting for food and drinks.  

## How to Participate
- **Attend a meeting**: Come to Venn Innovation on the first Friday at 6:30 PM.  
- **Present or demo**: If you’d like to give a short talk or demo, message the organizers on Discord or at the event. Talks can be technical, project-focused, or community-oriented.  
- **Share and collaborate**: Bring ideas, ask for feedback, or propose collaboration opportunities.  
- **Be welcoming**: Introduce yourself, listen, and be open to new perspectives.

---

## Code of Conduct and Contact
**Code of Conduct**  
- **Respect** everyone. Harassment, discrimination, or abusive behavior will not be tolerated.  
- If you experience or witness any issues, contact an organizer so we can address it promptly.

**Contact and Updates**  
- **Venue**: Venn Innovation, 770 St. George Boulevard.  
- **Announcements and schedule changes**: Posted on Discord and event listings.  
- **Organizers**: Reach out via the Discord server for organizer contact details and event coordination.

---

## Quick FAQ
- **Do I need to register**: No! Just show up and bring your smile! 
- **Can I bring a guest**: Yes, guests are welcome.  
- **Is there parking**: Venn Innovation has ample parking out front.  
- **Accessibility**: If you have accessibility needs, message the organizers on Discord so we can help.

---

## Scripts

### `scripts/add-meetup.py`

Adds a new meetup entry to the appropriate year's JSON and MD files. Creates the year directory and files if they don't exist yet.

```
python3 scripts/add-meetup.py [--date yyyy-mm-dd] [--time hh:mmam/pm] <topic> <presenter> [<presenter> ...]
```

**Arguments**

| Argument | Required | Default | Description |
|---|---|---|---|
| `topic` | yes | — | Talk title, as a quoted string |
| `presenter` | yes | — | One or more presenter names, each quoted |
| `--date` | no | Next first Friday of the month | Date in `yyyy-mm-dd` format |
| `--time` | no | `6:30pm` | Time in `h:mmam/pm` format |

**Examples**

```bash
# Add a talk for the next first Friday at 6:30 PM
python3 scripts/add-meetup.py "My crazy topic" "Alex Hart"

# Multiple presenters
python3 scripts/add-meetup.py "Panel discussion" "Alex Hart" "Michael Go" "Vincent Roy"

# Explicit date and time
python3 scripts/add-meetup.py --date 2026-05-01 --time 7:00pm "My crazy topic" "Alex Hart"

# Explicit date only (uses default 6:30 PM)
python3 scripts/add-meetup.py --date 2026-06-05 "Summer lightning talks" "Michael Go"
```

**Running the tests**

The pure helper functions have doctests. Run them with:

```bash
python3 -m doctest scripts/add-meetup.py
```

Add `-v` for verbose output showing each test case.
