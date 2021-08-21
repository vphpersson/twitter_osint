from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def cursor_id_to_datetime(cursor_id: int) -> datetime:
    """
    Attempt to convert a Twitter API cursor ID to a `datetime` value.

    The approach of obtaining a date and time from a cursor ID is only approximate; what the cursor IDs constitute is
    unclear. Why this works somewhat is unknown to me.

    :param cursor_id: A cursor ID to be converted to a datetime value.
    :return: A datetime value that corresponds to the cursor ID.
    """

    reference_ts = 1_693_604_227
    reference_dt = datetime(year=2021, month=3, day=7, hour=19, minute=54, second=13, tzinfo=ZoneInfo('UTC'))

    cursor_ts = cursor_id // 1_000_000_000

    # NOTE: The fraction is a "magic number".
    return reference_dt + (360_000 / 377_483) * timedelta(seconds=(cursor_ts - reference_ts))
