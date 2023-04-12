import typing as t

from datetime import datetime


def timestamp_to_datetime(ts: t.Union[float, int]):
    """Convert timestamps to UTC datetime"""
    return datetime.utcfromtimestamp(ts)
