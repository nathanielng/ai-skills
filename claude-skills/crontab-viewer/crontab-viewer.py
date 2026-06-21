#!/usr/bin/env python3
"""Parse crontab -l and generate JSON + HTML dashboard."""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def parse_crontab() -> list[dict]:
    """Parse crontab -l output and return list of cron job dicts."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if result.returncode != 0:
            return []
        output = result.stdout
    except FileNotFoundError:
        return []

    jobs = []
    for line in output.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Parse cron line: min hour day month dow command
        parts = line.split(None, 5)
        if len(parts) < 6:
            continue

        minute, hour, day, month, dow, command = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]

        # Extract description from trailing comment
        description = ""
        if " # " in command:
            command, description = command.rsplit(" # ", 1)
            description = description.strip()

        # Interpret frequency
        freq = interpret_frequency(minute, hour, day, month, dow)

        jobs.append({
            "minute": minute,
            "hour": hour,
            "day_of_month": day,
            "month": month,
            "day_of_week": dow,
            "command": command,
            "description": description,
            "frequency": freq,
            "raw": line,
        })

    return sorted(jobs, key=lambda j: j["frequency"])


def interpret_frequency(minute: str, hour: str, day: str, month: str, dow: str) -> str:
    """Interpret a cron schedule and return human-readable frequency."""
    if minute == "*" and hour == "*" and day == "*" and month == "*" and dow == "*":
        return "Every minute"
    elif minute == "0" and hour == "*" and day == "*" and month == "*" and dow == "*":
        return "Hourly"
    elif minute == "0" and hour == "0" and day == "*" and month == "*" and dow == "*":
        return "Daily (midnight)"
    elif minute == "0" and hour == "0" and day == "1" and month == "*" and dow == "*":
        return "Monthly (1st)"
    elif minute == "0" and hour == "0" and dow == "0":
        return "Weekly (Sunday)"
    elif minute == "0" and hour == "0" and dow == "1":
        return "Weekly (Monday)"
    elif dow != "*":
        return f"Weekly ({dow})"
    elif day != "*":
        return f"Day {day} of month"
    elif hour != "*" and day == "*" and month == "*" and dow == "*":
        # Daily at specific time
        return f"Daily at {hour}:{minute.zfill(2)}"
    else:
        return "Custom"


def generate_html(jobs: list[dict]) -> str:
    """Generate HTML dashboard for cron jobs."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    import time
    tz = time.tzname[0] if time.localtime().tm_isdst == 0 else time.tzname[1]

    job_rows = ""

    if not jobs:
        job_rows = '<tr><td colspan="8" style="text-align:center;color:#888;">No cron jobs found</td></tr>'
    else:
        for job in jobs:
            desc_cell = f'<td><span class="desc">{html_escape(job["description"])}</span></td>' if job["description"] else '<td style="color:#666;">—</td>'
            job_rows += f'''    <tr>
      <td><code>{job['minute']}</code></td>
      <td><code>{job['hour']}</code></td>
      <td><code>{job['day_of_month']}</code></td>
      <td><code>{job['month']}</code></td>
      <td><code>{job['day_of_week']}</code></td>
      <td><span class="freq-badge">{job['frequency']}</span></td>
      {desc_cell}
      <td><code class="cmd">{html_escape(job['command'])}</code></td>
    </tr>\n'''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Crontab Viewer</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0f1117; color: #e2e8f0; min-height: 100vh; padding: 2rem; }}
  h1 {{ font-size: 1.5rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem; }}
  .subtitle {{ color: #475569; font-size: 0.85rem; margin-bottom: 2rem; }}
  .card {{ background: #1e2130; border: 1px solid #2d3348; border-radius: 12px; padding: 1.5rem; max-width: 1200px; }}
  .card-title {{ font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; margin-bottom: 1rem; }}

  .table-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
  th {{ text-align: left; color: #64748b; font-weight: 600; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; padding: 0.75rem 0.5rem; border-bottom: 1px solid #2d3348; }}
  td {{ padding: 0.6rem 0.5rem; border-bottom: 1px solid #1a1f2e; color: #94a3b8; }}
  tr:hover {{ background: #252a3a; }}

  code {{ background: #0a0e16; border: 1px solid #2d3348; border-radius: 4px; padding: 0.2rem 0.4rem; font-family: "Monaco", "Courier New", monospace; font-size: 0.8rem; color: #e2e8f0; }}
  .cmd {{ display: block; max-width: 400px; overflow: auto; word-break: break-all; }}
  .freq-badge {{ display: inline-block; font-size: 0.7rem; background: #1e40af; color: #93c5fd; border-radius: 4px; padding: 0.25rem 0.5rem; white-space: nowrap; }}
  .desc {{ color: #cbd5e1; font-size: 0.85rem; font-weight: 500; }}

  .stats {{ display: flex; gap: 2rem; margin-bottom: 1.5rem; flex-wrap: wrap; }}
  .stat {{ display: flex; flex-direction: column; gap: 0.25rem; }}
  .stat-label {{ font-size: 0.7rem; color: #64748b; }}
  .stat-value {{ font-size: 1.5rem; font-weight: 700; color: #e2e8f0; }}

  footer {{ margin-top: 2rem; font-size: 0.7rem; color: #334155; }}
</style>
</head>
<body>

<h1>Crontab Viewer</h1>
<p class="subtitle">Generated {now} · Timezone: {tz}</p>

<div class="card">
  <div class="card-title">Cron Jobs Summary</div>
  <div class="stats">
    <div class="stat">
      <span class="stat-label">Total jobs</span>
      <span class="stat-value">{len(jobs)}</span>
    </div>
  </div>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Min</th>
          <th>Hour</th>
          <th>Day</th>
          <th>Month</th>
          <th>DoW</th>
          <th>Frequency</th>
          <th>Description</th>
          <th>Command</th>
        </tr>
      </thead>
      <tbody>
{job_rows}      </tbody>
    </table>
  </div>
</div>

<footer>Crontab: {len(jobs)} job{'s' if len(jobs) != 1 else ''} · Data: crontab -l</footer>

</body>
</html>"""


def html_escape(text: str) -> str:
    """Escape HTML special characters."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def main():
    jobs = parse_crontab()

    # Output JSON
    output_dir = Path(__file__).parent
    json_file = output_dir / "crontab.json"
    html_file = output_dir / "crontab.html"

    json_file.write_text(json.dumps(jobs, indent=2))
    html_file.write_text(generate_html(jobs))

    print(f"✅  Crontab parsed: {len(jobs)} jobs")
    print(f"📄  JSON → {json_file.name}")
    print(f"🌐  HTML → {html_file.name}")
    print(f"\nOpen in browser: file://{html_file.absolute()}")


if __name__ == "__main__":
    main()
