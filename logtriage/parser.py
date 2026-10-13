import re
from dataclasses import dataclass

LEVEL = re.compile(r"\b(DEBUG|INFO|WARN(?:ING)?|ERROR|CRITICAL|FATAL)\b", re.I)
IP = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
LONG_NUM = re.compile(r"\b\d{4,}\b")
UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f-]{27,}\b", re.I)

@dataclass(frozen=True)
class ParsedLine:
    level: str
    message: str
    pattern: str

def normalize_pattern(message):
    value = message.strip().lower()
    value = UUID.sub("<uuid>", value)
    value = IP.sub("<ip>", value)
    value = LONG_NUM.sub("<number>", value)
    value = re.sub(r'"[^"]*"', '"<text>"', value)
    return re.sub(r"\s+", " ", value) or "<empty>"

def parse_line(line):
    match = LEVEL.search(line)
    level = match.group(1).upper() if match else "UNKNOWN"
    message = line.strip()
    if match:
        message = (message[:match.start()] + message[match.end():]).strip(" :-\t")
    message = re.sub(r"^\[?\d{4}-\d\d-\d\d[T ][^\]\s]+\]?\s*", "", message)
    message = message or line.strip()
    return ParsedLine(level, message, normalize_pattern(message))
