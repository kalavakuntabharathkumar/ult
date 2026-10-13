import sqlite3
from logtriage.cli import analyze

def test_analyze_persists(tmp_path):
    log = tmp_path / "sample.log"
    log.write_text("ERROR disk full\nERROR disk full\nINFO ready\n", encoding="utf-8")
    db = tmp_path / "triage.db"
    result = analyze(str(log), db_path=str(db))
    assert result["processed_lines"] == 3
    conn = sqlite3.connect(db)
    assert conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0] == 1
    assert conn.execute("SELECT SUM(count) FROM pattern_counts").fetchone()[0] == 3
    conn.close()
