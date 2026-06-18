# crontab-viewer

Parse your crontab and view all cron jobs in an interactive HTML dashboard. Also exports to JSON for scripting.

## Invocation

```
/crontab-viewer
```

## Implementation

Script: `crontab-viewer.py`

Requires: `crontab` command (standard on macOS/Linux)

## What it does

1. Runs `crontab -l` to fetch all scheduled jobs
2. Parses each cron line (minute, hour, day, month, dow, command)
3. Interprets the frequency (hourly, daily, weekly, custom)
4. Generates two outputs:
   - **JSON** (`crontab.json`) — structured data for scripting
   - **HTML** (`crontab.html`) — interactive dashboard with color-coded frequency badges

## Output files

- `crontab.json` — array of parsed cron jobs with frequency interpretation
- `crontab.html` — dark-themed dashboard, opens in default browser

## Example JSON output

```json
[
  {
    "minute": "0",
    "hour": "9",
    "day_of_month": "*",
    "month": "*",
    "day_of_week": "*",
    "command": "/usr/local/bin/backup.sh",
    "frequency": "Daily",
    "raw": "0 9 * * * /usr/local/bin/backup.sh"
  }
]
```

## Running manually

```bash
python crontab-viewer.py
```

## Notes

- Comments (`#`) and blank lines in crontab are skipped
- Frequency is interpreted from the cron schedule (`* * * * *` format)
- If you have no cron jobs, the dashboard will show "No cron jobs found"
- Both JSON and HTML are regenerated every time you run the script
