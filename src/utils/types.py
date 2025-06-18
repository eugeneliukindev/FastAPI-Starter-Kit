from enum import StrEnum


class LogLevelEnum(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ModeEnum(StrEnum):
    DEV = "DEV"
    TEST = "TEST"
    PROD = "PROD"
