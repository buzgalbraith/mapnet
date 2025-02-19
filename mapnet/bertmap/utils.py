import datetime


def get_current_date_ymd():
    """Returns the current date as a string in YYYY_MM_DD format."""
    now = datetime.datetime.now()
    return now.strftime("%Y_%m_%d")
