'''
Created on 3 Aug 2021
@author: qsong
'''
import requests as requests
import unittest
from bs4 import BeautifulSoup
import psycopg2 as psycopg2
from src import utils

class wh_message(object):
    '''
    This module provides wuhu20888 functions
    '''
    game_base_url = "http://www.qq1099.com"

    def __init__(self):
        '''
        Constructor
        '''
        self.postgre_conn = psycopg2.connect(
            host="192.168.31.203",
            database="qwin",
            user="postgres",
            password="admin")
        self.postgre_cur = self.postgre_conn.cursor()
        return

    def __del__(self):
        return

    def add_message_to_db (self, message):

        user_name = message.get('wh_message_provider') + "_wh"
        print(user_name)
        sql = """SELECT user_id FROM users WHERE user_name = %s;				
                """
        self.postgre_cur.execute(sql, (user_name,))
        user_id = self.postgre_cur.fetchall()
        user_id_int = user_id[0][0]

        sql = """INSERT INTO messages (user_id, message_time, message_content, message_link)
                 SELECT %s, %s, %s, %s
                 WHERE NOT EXISTS (SELECT * FROM messages WHERE user_id = % AND message_time = %s);
                 """
        self.postgre_cur.execute(sql, (user_id, message.get('wh_message_time'), message.get('wh_message_text'),
                                       message.get('wh_message_link'), user_id, message.get('wh_message_time') ))
        # user_records = cur.fetchall()
        # print('user_records')
        return

    def add_user_to_db (self, user_name):
        user_name = user_name + "_wh"
        sql = """INSERT INTO users (user_name, notification) 
                SELECT %s, false
                WHERE NOT EXISTS (SELECT * FROM users WHERE user_name = %s);				
                """
        self.postgre_cur.execute(sql, (user_name, user_name))
        return

    def get_wh_message(self):
        wh_response = requests.get(self.game_base_url)
        wh_response = wh_response
        if wh_response.status_code == 200:
            soup = BeautifulSoup(wh_response.content, 'html.parser', from_encoding="gb18030")
            soup.prettify()
            ul_table = soup.find('ul')
            li_list = ul_table.find_all('li')
            wh_message = {}
            for li_item in li_list:
                if len(li_item.contents) >= 5:
                    wh_message['wh_message_provider'] =  li_item.contents[-3].contents[0]
                    wh_message['wh_message_time'] =  li_item.contents[-2].replace('】', '')
                    wh_message['wh_message_time_int'] = utils.convert_time_to_int(wh_message['wh_message_time'])
                    wh_message['wh_message_text'] =  li_item.contents[-5].contents[0]
                    wh_message['wh_message_link'] =  li_item.contents[-5].attrs['href']
                    self.add_user_to_db(wh_message['wh_message_provider'])
                    # self.add_message_to_db(wh_message)

            self.postgre_conn.commit()
            self.postgre_conn.close()
        return li_list

class Test(unittest.TestCase):

    def setUp(self):
        self.test_obj = wh_message()

    def tearDown(self):
        self.test_obj = None
        return

    def test_get_wuhu_message(self):
        self.test_obj.get_wh_message()
        return