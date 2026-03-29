# Travel Planner Agent

Builds **day-by-day trip outlines** from constraints (pace, budget band, interests). **No live bookings**—users must verify hours, prices, and entry rules on official sources.

```bash
cd "travel planner agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Your destination, dates, and style..."
```

Environment: `TRAVEL_PLANNER_AGENT_PROVIDER`, `TRAVEL_PLANNER_AGENT_MODEL`.
