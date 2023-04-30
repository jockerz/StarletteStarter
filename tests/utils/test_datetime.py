from datetime import datetime

from apps.utils.datetime import timestamp_to_datetime

TS = datetime.now().timestamp()


class TestTimestampsToDatetime:
    async def test_timestamp_to_datetime(self):
        assert isinstance(timestamp_to_datetime(TS), datetime)
        assert isinstance(timestamp_to_datetime(int(TS)), datetime)
