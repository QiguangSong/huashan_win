'''
Created on 3 Aug 2021
@author: qsong
'''
from datetime import datetime
import requests as requests
import unittest
from bs4 import BeautifulSoup
import psycopg2 as psycopg2
from src import utils


# from lxml.cssselect import CSSSelector
# import lxml.html

class sh_message(object):
    '''
    This module provides http://www.236666.net/ functions
    '''
    game_base_url = "http://www.236666.net"

    def __init__(self):
        '''
        Constructor
        '''
        self.postgre_conn = psycopg2.connect(
            host="192.168.31.158",
            database="qwin",
            user="postgres",
            password="admin")
        self.postgre_cur = self.postgre_conn.cursor()
        return

    def __del__(self):
        return

    def add_message_to_db (self, message):

        user_name = message.get('sh_message_provider') + "_sH"
        print(user_name)
        sql = """SELECT user_id FROM users WHERE user_name = %s;				
                """
        self.postgre_cur.execute(sql, (user_name,))
        user_id = self.postgre_cur.fetchall()
        user_id_int = user_id[0][0]

        sql = """INSERT INTO messages (user_id, message_time, message_content, message_link)
                 SELECT %s, %s, %s, %s
                 WHERE NOT EXISTS (SELECT * FROM messages WHERE user_id = %s AND message_time = %s);
                 """
        self.postgre_cur.execute(sql, (user_id_int, str(message.get('sh_message_time')), message.get('sh_message_text'),
                                       message.get('sh_message_link'), user_id_int, str(message.get('sh_message_time')) ))
        # user_records = cur.fetchall()
        # print('user_records')
        return

    def add_user_to_db(self, user_name):
        user_name = user_name + "_sH"
        sql = """INSERT INTO users (user_name, notification) 
                SELECT %s, false
                WHERE NOT EXISTS (SELECT * FROM users WHERE user_name = %s);				
                """
        self.postgre_cur.execute(sql, (user_name, user_name))
        return

    def get_sh_message(self):
        sh_response = requests.get(self.game_base_url, stream=True)

        if sh_response.status_code == 200:
            soup = BeautifulSoup(sh_response.content, 'html.parser', from_encoding="gb18030")
            soup.prettify()
            tbody_table = soup.select('body > table:nth-child(8)')


            li_list = tbody_table[0].find_all('li')

            sh_message = {}
            for li_item in li_list:
                if len(li_item.contents) >= 2:
                    user_time = li_item.contents[-1]

                    time_str = ("2022-" + user_time.split('】 ')[1] + " :00")
                    sh_message['sh_message_time'] = datetime.strptime(time_str, '%Y-%m-%d %H:%M  :%S').strftime("%Y%m%d%H%M%S")

                    sh_message['sh_message_time_int'] =utils.convert_time_to_int(sh_message['sh_message_time'])
                    sh_message['sh_message_provider'] = user_time.split('】')[0].replace('【', '').replace(' ', '')
                    sh_message['sh_message_text'] = li_item.contents[-2].contents[0]
                    sh_message['sh_message_link'] = li_item.contents[-2].attrs['href']
                    sh_message['platform'] = "sheHuo"
                    
                    self.add_user_to_db(sh_message['sh_message_provider'])
                    self.add_message_to_db(sh_message)

            self.postgre_conn.commit()
            self.postgre_conn.close()
        return li_list

class Test(unittest.TestCase):

    def setUp(self):
        self.test_obj = sh_message()

    def tearDown(self):
        self.test_obj = None
        return

    def test_get_sh_message(self):
        self.test_obj.get_sh_message()
        return
