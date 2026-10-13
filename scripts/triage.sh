#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 ]]; then echo "Usage: $0 LOGFILE [TOP_N]" >&2; exit 2; fi
logfile="$1"; top="${2:-5}"
if [[ ! -r "$logfile" ]]; then echo "Cannot read log file: $logfile" >&2; exit 1; fi
echo "== Severity counts (grep/awk) =="
grep -Eio '\b(DEBUG|INFO|WARN(ING)?|ERROR|CRITICAL|FATAL)\b' "$logfile" |
  awk '{ counts[toupper($0)]++ } END { for (level in counts) print counts[level], level }' | sort -nr || true
echo "== Top patterns (Python) =="
python -m logtriage.cli analyze "$logfile" --top "$top"
