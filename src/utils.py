import datetime
import re

game_base_url = "https://wh20888.com/"


def __init__(self):
    """
    Constructor
    """

    return


def __del__(self):
    return


def convert_time_to_int(time_str):
    time_int = int(re.sub(r'[^\w]', ' ', time_str).replace(' ',''))
    return time_int
