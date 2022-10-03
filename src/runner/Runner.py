"""
Created on 1 Oct 2022
@author: qsong
"""

import schedule as schedule
import sys
sys.path.append('../../src')
import unittest
from src.game_provider.huashan import huanshan_message
import time

class GameRunner(object):
    """
    This module provides huanshan functions
    """

    def __init__(self):
        self.get_message = huanshan_message()

    def GameRunnerJob(self):
        while True:
            self.get_message.get_huashan_message()
            time.sleep(600)
        return



class Test(unittest.TestCase):

    def setUp(self):
        self.test_obj = GameRunner()

    def tearDown(self):
        self.test_obj = None
        return

    def test_GameRunner(self):
        self.test_obj.GameRunnerJob()
        return
