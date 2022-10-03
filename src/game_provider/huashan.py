'''
Created on 3 Aug 2021
@author: qsong
'''
from datetime import datetime, timedelta

import requests as requests
import unittest
from bs4 import BeautifulSoup
import re


class huanshan_message(object):
    '''
    This module provides huanshan functions
    '''
    game_base_url = "https://bbs.hszqb2.com/bbs-1.html"
    FAV_LIST = ["华山小仙女", "东北球王"]

    def __init__(self):
        '''
        Constructor
        '''
        return

    def __del__(self):
        return

    def get_huashan_message(self):
        huanshan_response = requests.get(self.game_base_url)
        if huanshan_response.status_code == 200:
            soup = BeautifulSoup(huanshan_response.content, 'html.parser', from_encoding="gb18030")
            soup.prettify()
            ul_table = soup.find('ul')
            li_list = ul_table.find_all('li')
            now = datetime.now() - timedelta(hours=6, minutes=10)

            now_int = int(now.strftime("%Y%m%d%H%M%S"))
            print("date and time ==========================", str(now_int))
            for li_item in li_list:
                if len(li_item.contents) > 3:
                    message_time = int(''.join(re.findall(r'[0-9]+', li_item.contents[-2].text)))
                    game_name = li_item.contents[-3].text
                    message_context = li_item.contents[-5].text
                    if game_name in self.FAV_LIST and message_time > now_int:
                        print("time = " + str(message_time))  # time
                        print("name = " + game_name)  # name
                        print("message = " + message_context)  # message
                        print("---------------")
        return li_list


class Test(unittest.TestCase):

    def setUp(self):
        self.test_obj = huanshan_message()

    def tearDown(self):
        self.test_obj = None
        return

    def test_get_huanshan_message(self):
        self.test_obj.get_huashan_message()
        return
