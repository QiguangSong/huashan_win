
from datetime import datetime
import pytz
import unittest

class huashan_common(object):
    '''
    This module provides huanshan share functions
    '''

    def __init__(self):
        '''
        Constructor
        '''
        return

    def __del__(self):
        return

    def time_convert(self, gmt8_time):
        # Parse the input time string in GMT+8 timezone
        gmt8_timezone = pytz.timezone('Asia/Shanghai')
        gmt8_datetime = datetime.strptime(gmt8_time, "%Y%m%d%H%M%S")
        gmt8_datetime = gmt8_timezone.localize(gmt8_datetime)

        # Convert to CET timezone
        cet_timezone = pytz.timezone('CET')  # Central European Time
        cet_datetime = gmt8_datetime.astimezone(cet_timezone)

        # Format the CET time as required
        cet_time = cet_datetime.strftime("%Y%m%d%H%M%S")
#        print(cet_time)
        return cet_time




class Test(unittest.TestCase):

    def setUp(self):
        self.test_obj = huashan_common()

    def tearDown(self):
        self.test_obj = None
        return

    def test_get_huanshan_message(self):
        self.test_obj.time_convert("20240117025107")
        return
