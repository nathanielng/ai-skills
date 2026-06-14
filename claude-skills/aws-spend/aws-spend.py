#!/usr/bin/env python3
"""AWS spend report with caching. Fetches only missing days on each run."""

import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).parent
CACHE_FILE = SKILL_DIR / "cache.json"
HTML_OUT = SKILL_DIR / "aws-spend-dashboard.html"
CE_REGION = "us-east-1"

def get_account_id() -> str:
    r = subprocess.run(["aws", "sts", "get-caller-identity", "--query", "Account", "--output", "text"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else "unknown"

ACCOUNT = get_account_id()

EXCL_CREDITS = json.dumps({"Not": {"Dimensions": {"Key": "RECORD_TYPE", "Values": ["Credit"]}}})

# Load credit grants from credits.json if present (gitignored — contains personal billing data)
# Format: [{"id": "...", "name": "...", "issued": 25.00, "start": "...", "expiry": "...", "used": 0.00, "remaining": 25.00}]
_credits_file = SKILL_DIR / "credits.json"
CREDIT_GRANTS = json.loads(_credits_file.read_text()) if _credits_file.exists() else []


# ---------------------------------------------------------------------------
# AWS helpers
# ---------------------------------------------------------------------------

def run_aws(*args):
    cmd = ["aws", "--output", "json"] + list(args)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"AWS ERROR: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout)


def ce_daily(start, end, group_key, filter_json=None):
    args = ["ce", "get-cost-and-usage",
            "--region", CE_REGION,
            "--time-period", f"Start={start},End={end}",
            "--granularity", "DAILY",
            "--metrics", "UnblendedCost",
            "--group-by", f"Type=DIMENSION,Key={group_key}"]
    if filter_json:
        args += ["--filter", filter_json]
    return run_aws(*args)


def ce_monthly_total(start, end, filter_json=None):
    args = ["ce", "get-cost-and-usage",
            "--region", CE_REGION,
            "--time-period", f"Start={start},End={end}",
            "--granularity", "MONTHLY",
            "--metrics", "UnblendedCost"]
    if filter_json:
        args += ["--filter", filter_json]
    return run_aws(*args)


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

def load_cache():
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except Exception:
            pass
    return {"month": "", "service": {}, "usage_type": {}, "gross": {}}


def save_cache(c):
    CACHE_FILE.write_text(json.dumps(c, indent=2))


def refresh_cache(today, yesterday, month_start):
    month_key = str(month_start)[:7]
    cache = load_cache()

    if cache.get("month") != month_key:
        print(f"  New month ({month_key}), resetting cache.", file=sys.stderr)
        cache = {"month": month_key, "service": {}, "usage_type": {}, "gross": {}}

    needed = []
    d = month_start
    while d <= yesterday:
        if str(d) not in cache["service"]:
            needed.append(str(d))
        d += timedelta(days=1)

    if needed:
        fetch_start = needed[0]
        fetch_end = str(date.fromisoformat(needed[-1]) + timedelta(days=1))
        print(f"  Fetching {len(needed)} new day(s) ({fetch_start} → {needed[-1]})...", file=sys.stderr)

        r_svc   = ce_daily(fetch_start, fetch_end, "SERVICE",    EXCL_CREDITS)
        r_usage = ce_daily(fetch_start, fetch_end, "USAGE_TYPE", EXCL_CREDITS)
        r_gross = ce_daily(fetch_start, fetch_end, "SERVICE")  # includes credits → net after credits

        for result in r_svc["ResultsByTime"]:
            day = result["TimePeriod"]["Start"]
            cache["service"][day] = {
                g["Keys"][0]: round(float(g["Metrics"]["UnblendedCost"]["Amount"]), 6)
                for g in result["Groups"]
            }

        for result in r_usage["ResultsByTime"]:
            day = result["TimePeriod"]["Start"]
            cache["usage_type"][day] = {
                g["Keys"][0]: round(float(g["Metrics"]["UnblendedCost"]["Amount"]), 6)
                for g in result["Groups"]
            }

        for result in r_gross["ResultsByTime"]:
            day = result["TimePeriod"]["Start"]
            cache["gross"][day] = round(
                sum(float(g["Metrics"]["UnblendedCost"]["Amount"]) for g in result["Groups"]), 6
            )

        save_cache(cache)
        print(f"  Cache saved ({len(cache['service'])} days cached).", file=sys.stderr)
    else:
        print(f"  Cache up to date ({len(cache['service'])} days).", file=sys.stderr)

    return cache


# ---------------------------------------------------------------------------
# CLI report
# ---------------------------------------------------------------------------

def fmt(v):
    return f"${v:,.2f}"


def print_report(cache, today, yesterday, month_start):
    col_w = 42

    print(f"\n{'='*58}")
    print(f"  AWS SPEND REPORT  —  account {ACCOUNT}")
    print(f"{'='*58}")

    # Yesterday
    yd = str(yesterday)
    svc_yd = cache["service"].get(yd, {})
    gross_yd = cache["gross"].get(yd, 0.0)
    net_yd = sum(v for v in svc_yd.values() if v > 0)
    credits_yd = gross_yd - net_yd

    print(f"\n📅 Yesterday ({yesterday})  —  Top services (excl. credits)\n")
    top = sorted(((k, v) for k, v in svc_yd.items() if v >= 0.005), key=lambda x: -x[1])[:10]
    if not top:
        print("  (no charges)")
    for i, (svc, amt) in enumerate(top, 1):
        print(f"  {i}. {fmt(amt)}  {svc}")
    print(f"\n  {'Yesterday (excl. credits)':<{col_w+6}}  {fmt(net_yd):>10}")
    if credits_yd:
        print(f"  {'Credits applied':<{col_w+6}}  {fmt(credits_yd):>10}")
    print(f"  {'Yesterday (incl. credits)':<{col_w+6}}  {fmt(gross_yd):>10}")

    # MTD
    all_days = sorted(cache["service"].keys())
    net_mtd = sum(sum(v for v in cache["service"][d].values() if v > 0) for d in all_days)
    gross_mtd = sum(cache["gross"].get(d, 0) for d in all_days)
    credits_mtd = gross_mtd - net_mtd

    # MTD by service
    svc_mtd = {}
    for d in all_days:
        for svc, amt in cache["service"][d].items():
            svc_mtd[svc] = svc_mtd.get(svc, 0) + amt
    top_mtd = sorted(((k, v) for k, v in svc_mtd.items() if v >= 0.005), key=lambda x: -x[1])[:10]

    print(f"\n{'─'*58}")
    print(f"\n📆 Month to date ({month_start} → {yesterday})  —  Top services (excl. credits)\n")
    for i, (svc, amt) in enumerate(top_mtd, 1):
        print(f"  {i}. {fmt(amt)}  {svc}")
    print(f"\n  {'MTD (excl. credits)':<{col_w+6}}  {fmt(net_mtd):>10}")
    if credits_mtd:
        print(f"  {'Credits applied':<{col_w+6}}  {fmt(credits_mtd):>10}")
    print(f"  {'MTD (incl. credits)':<{col_w+6}}  {fmt(gross_mtd):>10}")
    print(f"\n{'='*58}\n")


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

def build_html(cache, today, yesterday, month_start):
    all_days = sorted(cache["service"].keys())

    # --- Chart data ---
    yd = str(yesterday)
    svc_yd = cache["service"].get(yd, {})
    gross_yd = cache["gross"].get(yd, 0.0)
    net_yd = sum(v for v in svc_yd.values() if v > 0)
    credits_yd = gross_yd - net_yd

    top_yd = sorted(((k, v) for k, v in svc_yd.items() if v >= 0.005), key=lambda x: -x[1])[:10]
    max_yd = top_yd[0][1] if top_yd else 1

    svc_mtd = {}
    for d in all_days:
        for svc, amt in cache["service"][d].items():
            svc_mtd[svc] = svc_mtd.get(svc, 0) + amt
    top_mtd = sorted(((k, v) for k, v in svc_mtd.items() if v >= 0.005), key=lambda x: -x[1])[:10]
    max_mtd = top_mtd[0][1] if top_mtd else 1

    net_mtd = sum(sum(v for v in cache["service"][d].values() if v > 0) for d in all_days)
    gross_mtd = sum(cache["gross"].get(d, 0) for d in all_days)
    credits_mtd = gross_mtd - net_mtd

    # --- Table data (usage type × day) ---
    all_usage_types = set()
    for d in all_days:
        all_usage_types.update(cache["usage_type"].get(d, {}).keys())

    usage_mtd = {}
    for ut in all_usage_types:
        usage_mtd[ut] = sum(cache["usage_type"].get(d, {}).get(ut, 0) for d in all_days)

    usage_rows = sorted(all_usage_types, key=lambda ut: -usage_mtd[ut])

    # Daily totals row
    daily_totals = {d: sum(v for v in cache["usage_type"].get(d, {}).values() if v > 0) for d in all_days}

    # Credit grant totals
    total_issued    = sum(g["issued"]    for g in CREDIT_GRANTS)
    total_used      = sum(g["used"]      for g in CREDIT_GRANTS)
    total_remaining = sum(g["remaining"] for g in CREDIT_GRANTS)

    # --- Build HTML ---
    day_headers = "".join(
        f'<th>{date.fromisoformat(d).strftime("%-d %b")}</th>' for d in all_days
    )

    daily_total_cells = "".join(
        f'<td class="num">{fmt(daily_totals.get(d, 0))}</td>' for d in all_days
    )

    usage_rows_html = ""
    for ut in usage_rows:
        mtd = usage_mtd[ut]
        if mtd < 0.001:
            continue
        cells = "".join(
            f'<td class="num">{fmt(cache["usage_type"].get(d, {}).get(ut, 0)) if cache["usage_type"].get(d, {}).get(ut, 0) >= 0.001 else "−"}</td>'
            for d in all_days
        )
        usage_rows_html += f'<tr><td class="ut-label">{ut}</td><td class="num mtd-col">{fmt(mtd)}</td>{cells}</tr>\n'

    def bar_rows(items, max_val, region_map=None):
        html = ""
        for i, (svc, amt) in enumerate(items, 1):
            w = round(amt / max_val * 100)
            region = region_map.get(svc, "") if region_map else ""
            region_span = f'<span class="bar-region">{region}</span>' if region else ""
            html += f'''      <div class="bar-row">
        <span class="bar-rank">{i}</span>
        <span class="bar-label">{svc}</span>
        {region_span}
        <div class="bar-track"><div class="bar-fill" style="width:{w}%"></div></div>
        <span class="bar-amount">{fmt(amt)}</span>
      </div>\n'''
        return html

    credit_rows_html = ""
    for g in CREDIT_GRANTS:
        credit_rows_html += f'''        <tr>
          <td>{g["id"]}</td>
          <td class="name">{g["name"]}</td>
          <td>{fmt(g["issued"])}</td>
          <td>{g["start"]}</td>
          <td>{g["expiry"]}</td>
          <td><span class="badge">✓ Active</span></td>
          <td class="right amber">{fmt(g["used"])}</td>
          <td class="right green">{fmt(g["remaining"])}</td>
        </tr>\n'''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AWS Spend — {today}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0f1117; color: #e2e8f0; min-height: 100vh; padding: 2rem; }}
  h1 {{ font-size: 1.25rem; font-weight: 600; color: #94a3b8; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.25rem; }}
  .subtitle {{ color: #475569; font-size: 0.85rem; margin-bottom: 1.5rem; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; max-width: 1100px; }}
  @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  .card {{ background: #1e2130; border: 1px solid #2d3348; border-radius: 12px; padding: 1.5rem; }}
  .card-title {{ font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; margin-bottom: 1rem; }}
  .card.wide {{ grid-column: 1 / -1; }}

  /* Toggle */
  .toolbar {{ display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1.5rem; max-width: 1100px; }}
  .toolbar span {{ color: #475569; font-size: 0.8rem; margin-right: 0.25rem; }}
  .toggle-btn {{ font-size: 0.75rem; font-weight: 600; padding: 0.35rem 0.9rem; border-radius: 6px; border: 1px solid #2d3348; background: #1e2130; color: #64748b; cursor: pointer; }}
  .toggle-btn.active {{ background: #3b82f6; border-color: #3b82f6; color: #fff; }}

  /* Summary totals */
  .totals {{ display: flex; gap: 2rem; flex-wrap: wrap; }}
  .total-item {{ flex: 1; min-width: 140px; }}
  .total-label {{ font-size: 0.75rem; color: #64748b; margin-bottom: 0.25rem; }}
  .total-value {{ font-size: 1.75rem; font-weight: 700; }}
  .total-value.green {{ color: #10b981; }}
  .total-value.amber {{ color: #f59e0b; }}
  .total-value.muted {{ color: #475569; }}
  .credit-badge-inline {{ display: inline-block; font-size: 0.7rem; background: #064e3b; color: #10b981; border-radius: 4px; padding: 1px 6px; margin-left: 6px; vertical-align: middle; }}

  /* Bar chart */
  .bar-list {{ display: flex; flex-direction: column; gap: 0.75rem; }}
  .bar-row {{ display: flex; align-items: center; gap: 0.75rem; }}
  .bar-rank {{ font-size: 0.7rem; color: #475569; width: 1.2rem; text-align: right; flex-shrink: 0; }}
  .bar-label {{ font-size: 0.8rem; color: #94a3b8; width: 210px; flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .bar-region {{ font-size: 0.75rem; color: #475569; width: 110px; flex-shrink: 0; }}
  .bar-track {{ flex: 1; background: #2d3348; border-radius: 4px; height: 8px; overflow: hidden; }}
  .bar-fill {{ height: 100%; border-radius: 4px; background: linear-gradient(90deg, #3b82f6, #6366f1); }}
  .bar-amount {{ font-size: 0.8rem; font-weight: 600; color: #e2e8f0; width: 3.5rem; text-align: right; flex-shrink: 0; }}

  /* MTD donut */
  .mtd-inner {{ display: flex; align-items: center; gap: 2rem; }}
  .donut-wrap {{ position: relative; width: 100px; height: 100px; flex-shrink: 0; }}
  svg.donut {{ transform: rotate(-90deg); }}
  .donut-center {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 0.65rem; color: #64748b; text-align: center; }}
  .mtd-stats {{ display: flex; flex-direction: column; gap: 0.75rem; }}
  .stat-row {{ display: flex; flex-direction: column; }}
  .stat-label {{ font-size: 0.7rem; color: #64748b; }}
  .stat-value {{ font-size: 1rem; font-weight: 700; color: #e2e8f0; }}
  .stat-value.credit {{ color: #10b981; }}

  /* Credits grants */
  .credits-disclaimer {{ font-size: 0.7rem; color: #475569; margin-bottom: 1rem; font-style: italic; }}
  .credits-summary {{ display: flex; gap: 2rem; margin-bottom: 1.25rem; flex-wrap: wrap; }}
  .credits-summary-item .lbl {{ font-size: 0.7rem; color: #64748b; }}
  .credits-summary-item .val {{ font-size: 1.4rem; font-weight: 700; }}
  .credits-table {{ width: 100%; border-collapse: collapse; font-size: 0.8rem; }}
  .credits-table th {{ text-align: left; color: #475569; font-weight: 600; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; padding: 0 0.75rem 0.5rem 0; border-bottom: 1px solid #2d3348; }}
  .credits-table th.right, .credits-table td.right {{ text-align: right; }}
  .credits-table td {{ padding: 0.6rem 0.75rem 0.6rem 0; color: #94a3b8; border-bottom: 1px solid #1a1f2e; }}
  .credits-table td.name {{ color: #e2e8f0; }}
  .credits-table td.green {{ color: #10b981; font-weight: 600; }}
  .credits-table td.amber {{ color: #f59e0b; font-weight: 600; }}
  .badge {{ display: inline-flex; align-items: center; gap: 4px; font-size: 0.7rem; background: #064e3b; color: #10b981; border-radius: 4px; padding: 1px 6px; }}

  /* Usage table */
  .table-wrap {{ overflow-x: auto; }}
  .usage-table {{ border-collapse: collapse; font-size: 0.75rem; min-width: 100%; }}
  .usage-table th {{ position: sticky; top: 0; background: #1e2130; color: #64748b; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; padding: 0.5rem 0.6rem; border-bottom: 1px solid #2d3348; white-space: nowrap; text-align: right; }}
  .usage-table th.left {{ text-align: left; }}
  .usage-table td {{ padding: 0.45rem 0.6rem; border-bottom: 1px solid #1a1f2e; white-space: nowrap; color: #64748b; text-align: right; }}
  .usage-table td.ut-label {{ text-align: left; color: #94a3b8; font-size: 0.75rem; }}
  .usage-table td.num {{ color: #94a3b8; font-variant-numeric: tabular-nums; }}
  .usage-table td.mtd-col {{ color: #e2e8f0; font-weight: 600; }}
  .usage-table tr.total-row td {{ color: #e2e8f0; font-weight: 700; border-bottom: 2px solid #2d3348; }}
  .usage-table tr:hover td {{ background: #252a3a; }}

  footer {{ margin-top: 2rem; font-size: 0.7rem; color: #334155; max-width: 1100px; }}
</style>
</head>
<body>

<h1>AWS Spend Report</h1>
<p class="subtitle">Account {ACCOUNT} &nbsp;·&nbsp; ap-southeast-1 &nbsp;·&nbsp; Generated {today}</p>

<div class="toolbar">
  <span>View:</span>
  <button class="toggle-btn active" id="btn-charts" onclick="showView('charts')">Charts</button>
  <button class="toggle-btn"        id="btn-table"  onclick="showView('table')">Table</button>
</div>

<!-- CHARTS VIEW -->
<div id="view-charts">
<div class="grid">

  <!-- Yesterday summary -->
  <div class="card">
    <div class="card-title">Yesterday &nbsp;·&nbsp; {yesterday}</div>
    <div class="totals">
      <div class="total-item">
        <div class="total-label">Gross spend</div>
        <div class="total-value amber">{fmt(net_yd)}</div>
      </div>
      <div class="total-item">
        <div class="total-label">After credits</div>
        <div class="total-value green">{fmt(gross_yd)} <span class="credit-badge-inline">fully covered</span></div>
      </div>
      <div class="total-item">
        <div class="total-label">Credits applied</div>
        <div class="total-value muted">{fmt(credits_yd)}</div>
      </div>
    </div>
  </div>

  <!-- MTD summary -->
  <div class="card">
    <div class="card-title">Month to date &nbsp;·&nbsp; {month_start.strftime("%-d %b")} → {yesterday.strftime("%-d %b")}</div>
    <div class="mtd-inner">
      <div class="donut-wrap">
        <svg class="donut" width="100" height="100" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="38" fill="none" stroke="#2d3348" stroke-width="12"/>
          <circle cx="50" cy="50" r="38" fill="none" stroke="#10b981" stroke-width="12"
                  stroke-dasharray="238.76 0" stroke-linecap="round"/>
        </svg>
        <div class="donut-center">100%<br>covered</div>
      </div>
      <div class="mtd-stats">
        <div class="stat-row"><span class="stat-label">Gross spend</span><span class="stat-value">{fmt(net_mtd)}</span></div>
        <div class="stat-row"><span class="stat-label">Credits applied</span><span class="stat-value credit">{fmt(credits_mtd)}</span></div>
        <div class="stat-row"><span class="stat-label">Net cost</span><span class="stat-value">{fmt(gross_mtd)}</span></div>
      </div>
    </div>
  </div>

  <!-- Yesterday bar chart -->
  <div class="card wide">
    <div class="card-title">Yesterday — Top services (excl. credits) &nbsp;<span style="font-weight:400;color:#334155">· scale: {fmt(max_yd)} max</span></div>
    <div class="bar-list">
{bar_rows(top_yd, max_yd)}    </div>
  </div>

  <!-- MTD bar chart -->
  <div class="card wide">
    <div class="card-title">Month to date — Top services (excl. credits) &nbsp;<span style="font-weight:400;color:#334155">· scale: {fmt(max_mtd)} max</span></div>
    <div class="bar-list">
{bar_rows(top_mtd, max_mtd)}    </div>
  </div>

  <!-- Credit grants -->
  <div class="card wide">
    <div class="card-title">Active credit grants</div>
    <p class="credits-disclaimer">⚠ Snapshot from AWS Billing console on 14 Jun 2026 — amounts may have changed since.</p>
    <div class="credits-summary">
      <div class="credits-summary-item"><span class="lbl">Total remaining</span><span class="val" style="color:#10b981">{fmt(total_remaining)}</span></div>
      <div class="credits-summary-item"><span class="lbl">Total used</span><span class="val" style="color:#f59e0b">{fmt(total_used)}</span></div>
      <div class="credits-summary-item"><span class="lbl">Total issued</span><span class="val">{fmt(total_issued)}</span></div>
      <div class="credits-summary-item"><span class="lbl">Expiry</span><span class="val" style="font-size:1rem;padding-top:0.3rem;color:#94a3b8">31 Dec 2026</span></div>
    </div>
    <table class="credits-table">
      <thead>
        <tr><th>Credit ID</th><th>Name</th><th>Issued</th><th>Start</th><th>Expiry</th><th>Status</th><th class="right">Used</th><th class="right">Remaining</th></tr>
      </thead>
      <tbody>
{credit_rows_html}      </tbody>
    </table>
  </div>

</div>
</div>

<!-- TABLE VIEW -->
<div id="view-table" style="display:none">
<div class="grid">
  <div class="card wide">
    <div class="card-title">Cost and usage breakdown by usage type &nbsp;·&nbsp; {month_start.strftime("%-d %b")} → {yesterday.strftime("%-d %b")}</div>
    <div class="table-wrap">
      <table class="usage-table">
        <thead>
          <tr>
            <th class="left">Usage type</th>
            <th>MTD total</th>
            {day_headers}
          </tr>
        </thead>
        <tbody>
          <tr class="total-row">
            <td class="ut-label">Total costs</td>
            <td class="num mtd-col">{fmt(net_mtd)}</td>
            {daily_total_cells}
          </tr>
{usage_rows_html}        </tbody>
      </table>
    </div>
  </div>
</div>
</div>

<footer>Data source: AWS Cost Explorer · UnblendedCost · Generated {today}</footer>

<script>
function showView(v) {{
  document.getElementById('view-charts').style.display = v === 'charts' ? '' : 'none';
  document.getElementById('view-table').style.display  = v === 'table'  ? '' : 'none';
  document.getElementById('btn-charts').className = 'toggle-btn' + (v === 'charts' ? ' active' : '');
  document.getElementById('btn-table').className  = 'toggle-btn' + (v === 'table'  ? ' active' : '');
}}
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    today = date.today()
    yesterday = today - timedelta(days=1)
    month_start = today.replace(day=1)

    cache = refresh_cache(today, yesterday, month_start)
    print_report(cache, today, yesterday, month_start)

    html = build_html(cache, today, yesterday, month_start)
    HTML_OUT.write_text(html)
    print(f"  HTML → {HTML_OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
