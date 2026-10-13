import argparse
from collections import Counter, defaultdict
from pathlib import Path
from .parser import parse_line
from .algorithms import PrefixTrie, top_k, group_prefixes
from .storage import connect, save_run

def analyze(path, top=10, db_path="triage.db"):
    counts = Counter()
    levels = defaultdict(Counter)
    processed = 0
    # Read one line at a time to avoid loading the entire file into memory.
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue
            item = parse_line(line)
            counts[item.pattern] += 1
            levels[item.pattern][item.level] += 1
            processed += 1
    trie = PrefixTrie()
    for pattern, count in counts.items():
        trie.add(pattern, count)
    prefixes = group_prefixes(counts)
    conn = connect(db_path)
    rows = [(p, levels[p].most_common(1)[0][0], n) for p, n in counts.items()]
    run_id = save_run(conn, str(Path(path)), processed, rows)
    conn.close()
    return {"source": str(path), "processed_lines": processed, "unique_patterns": len(counts),
            "top": top_k(counts, top), "prefix_groups": sorted(prefixes.items(), key=lambda x: (-x[1], x[0]))[:top],
            "run_id": run_id}

def main():
    parser = argparse.ArgumentParser(description="Stream and summarize application logs")
    sub = parser.add_subparsers(dest="command", required=True)
    cmd = sub.add_parser("analyze")
    cmd.add_argument("logfile")
    cmd.add_argument("--top", type=int, default=10)
    cmd.add_argument("--db", default="triage.db")
    args = parser.parse_args()
    result = analyze(args.logfile, args.top, args.db)
    print(f"Source: {result['source']}")
    print(f"Processed lines: {result['processed_lines']}")
    print(f"Unique patterns: {result['unique_patterns']}")
    print(f"SQLite run id: {result['run_id']}")
    print("\nTop patterns:")
    for pattern, count in result["top"]:
        print(f"{count:>6}  {pattern}")
    print("\nPrefix groups:")
    for prefix, count in result["prefix_groups"]:
        print(f"{count:>6}  {prefix}")

if __name__ == "__main__":
    main()
