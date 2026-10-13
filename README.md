# Unix Log Triage and Release Automation Toolkit

Python/Bash log triage demo with streaming parsing, normalized error-pattern counts, trie prefix grouping, top-K ranking, SQLite persistence, a cron example, and pytest tests.

## Run (Windows PowerShell)
    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python -m logtriage.cli analyze samples/app.log --top 5 --db triage.db
    pytest -q

## Run (Ubuntu/Linux)
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python -m logtriage.cli analyze samples/app.log --top 5 --db triage.db
    pytest -q
    bash scripts/triage.sh samples/app.log 5

Cron example (edit paths for your server):
    15 2 * * * /usr/bin/python3 /opt/unix-log-triage-toolkit/run_daily.py analyze /var/log/myapp.log --db /var/lib/logtriage/triage.db >> /var/log/logtriage-cron.log 2>&1

Included logs are small fixtures. Resume scale/performance claims (2.4 GB/day, 1.2M lines, 94% coverage, collaboration metrics) are not represented as measured results by this demo; benchmark and verify them in your own environment.
