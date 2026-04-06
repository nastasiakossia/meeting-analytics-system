# Meeting Analytics System

Web-based analytical system for exploring meeting data, identifying high-risk participants, and uncovering patterns in observer behavior using SQL-driven insights.

---

## Overview

This project simulates a data analytics system for monitoring structured meeting activity.

The goal is to detect **risk patterns, behavioral anomalies, and monitoring gaps** using SQL-based analysis.

The system answers questions such as:
- Which participants are repeatedly involved in high-density meetings without being monitored?
- Which observers are the most reliable in complex environments?
- Where do inconsistencies between expected and recorded activity occur?

This reflects real-world data analysis tasks such as:
- anomaly detection
- risk scoring
- behavioral pattern analysis

---

## Key Features

- **Analytics Dashboard**
  - Identify high-risk participants based on meeting activity
  - Detect unmonitored participants in high-density meetings
  - Find observers with the highest confidence per meeting
  - Discover unusual meeting-location patterns

- **Add Observation**
  - Insert new observation records via validated forms
  - Uses dropdowns to prevent invalid inputs

-  **Participant Analysis**
  - Analyze individual participant activity and risk

-  **Location-Based Filtering**
  - Find participants by meeting location

---

## Technical Focus

This project emphasizes:

- Writing **complex SQL queries** for analytical tasks
- Designing and working with a **relational database schema**
- Integrating SQL logic into a **Django backend**
- Structuring code for clarity (separating queries from views)
- Building a clean and intuitive **user interface**

---

## Database

- Initially worked with a **university-provided database**
- Later **reconstructed the schema independently**
- Created and populated tables using:
  - `create_tables_commands.sql`
  - CSV datasets (`data/` folder)

---

## Tech Stack

- Python
- Django
- SQL (T-SQL / SQL Server)
- HTML, CSS

---

## Project Structure
```
meeting-analytics-system/
│
├── Meetings_App/
│ ├── views.py
│ ├── queries.py
│ ├── models.py
│ ├── urls.py
│ └── ...
│
├── config/
│ ├── settings.py
│ ├── urls.py
│ └── ...
│
├── templates/
├── static/
├── data/
│
├── manage.py
├── requirements.txt
├── create_tables_commands.sql
└── queries_views.sql
```

- `queries.py` — contains raw SQL logic
- `views.py` — connects backend to UI
- `templates/` — frontend pages
- `data/` — datasets used for population

---

## Screenshots

### Home Page
![Home](assets/home.png)

### Analytics Dashboard
![Home](assets/analysis.png)

### Add Observation
![Home](assets/add.png)

### Participant Analysis
![Home](assets/participants.png)

---

## Engineering Decisions

- Replaced free-text inputs with dropdowns to ensure **data integrity**
- Separated SQL queries into a dedicated module (`queries.py`)
- Unified naming across the project for consistency
- Improved UX and navigation clarity
- Designed queries to extract **meaningful insights**, not just raw data

---

## How to Run

```bash
pip install -r requirements.txt
python manage.py runserver
```
Make sure the database is configured in `settings.py`.

## Notes
- The project demonstrates data analysis through SQL, not machine learning
- Focus is on query design, relational thinking, and system integration

## Author

Anastasia Kondrus
Technion – Data Science & Cognitive Science
