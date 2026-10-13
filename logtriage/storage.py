import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 source TEXT NOT NULL,
 processed_lines INTEGER NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS pattern_counts (
 run_id INTEGER NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
 pattern TEXT NOT NULL,
 level TEXT NOT NULL,
 count INTEGER NOT NULL,
 PRIMARY KEY (run_id, pattern, level)
);
"""

def connect(path):
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
    return conn

def save_run(conn, source, processed_lines, rows):
    cur = conn.execute("INSERT INTO runs(source, processed_lines) VALUES (?, ?)",
                       (source, processed_lines))
    run_id = cur.lastrowid
    conn.executemany("INSERT INTO pattern_counts VALUES (?, ?, ?, ?)",
                     [(run_id, pattern, level, count) for pattern, level, count in rows])
    conn.commit()
    return run_id
