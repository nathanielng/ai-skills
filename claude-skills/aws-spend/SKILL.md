# AWS Spend Skill

Show AWS cost summary: yesterday's top 10 billing services and month-to-date total, with an HTML dashboard (chart + table views).

## Invocation

```
/aws-spend
```

## Requirements

- AWS CLI configured with credentials that have `ce:GetCostAndUsage` and `sts:GetCallerIdentity` permissions
- No extra Python dependencies — stdlib only

## What it shows

1. **Yesterday's top services** by UnblendedCost (excl. credits)
2. **Yesterday's total** with and without credits
3. **Month-to-date total** with and without credits
4. **HTML dashboard** with chart view and daily usage-type table view

## Optional: credit grants

Place a `credits.json` file (gitignored) in the skill directory to show active credit grants in the dashboard:

```json
[
  {"id": "...", "name": "...", "issued": 25.00, "start": "01 Jan 2026", "expiry": "31 Dec 2026", "used": 0.00, "remaining": 25.00}
]
```

## Caching

Daily spend data is cached in `cache.json` (gitignored). Only missing days are fetched from the Cost Explorer API on each run.

## Running manually

```bash
python aws-spend.py
```
