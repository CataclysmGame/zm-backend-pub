import datetime

from app.util import get_timestamp


def test_date_range():
    # Remove old records
    today = datetime.datetime.fromtimestamp(
        get_timestamp(),
        tz=datetime.timezone.utc
    )
    print(today.isoformat())
    tomorrow = today + datetime.timedelta(days=1)
    print(tomorrow.isoformat())

    start_datetime = datetime.datetime.combine(today, datetime.time(hour=14))

    print(start_datetime.isoformat())

    end_datetime = datetime.datetime.combine(tomorrow, datetime.time(hour=14))

    print(end_datetime.isoformat())

    start_date_timestamp = int(start_datetime.timestamp())
    end_date_timestamp = int(end_datetime.timestamp())

    print(start_date_timestamp)
    print(get_timestamp())
    print(end_date_timestamp)

    print(datetime.datetime.fromtimestamp(get_timestamp(), datetime.timezone.utc).isoformat())

    assert end_date_timestamp >= get_timestamp() >= start_date_timestamp
