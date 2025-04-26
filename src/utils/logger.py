from datetime import datetime, timezone
import logging


class LogfmtFormatter(logging.Formatter):
    def __get_log_string(self, log_record: dict) -> dict:
        parts = []
        for key, value in log_record.items():
            if isinstance(value, str) and (" " in value or "=" in value):
                value = f'"{value}"'
            parts.append(f"{key}={value}")
        return " ".join(parts)

    def format(self, record):
        log_record = {
            "level": record.levelname.lower(),
            "time": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "module": record.name,
            "line": record.lineno,
            "correlation_id": getattr(record, "correlation_id", "-"),
            "message": record.getMessage().replace('"', '\\"'),
        }
        return self.__get_log_string(log_record)
