from logtriage.parser import parse_line, normalize_pattern

def test_parse_and_normalize():
    item = parse_line("2026-10-12T10:00:00Z ERROR failed for host 10.0.0.1 id 123456")
    assert item.level == "ERROR"
    assert "<ip>" in item.pattern and "<number>" in item.pattern

def test_unknown_and_empty():
    assert parse_line("application ready").level == "UNKNOWN"
    assert normalize_pattern("  ") == "<empty>"
