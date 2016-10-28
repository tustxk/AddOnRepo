# coding=utf-8
import unittest
from mediathek.ard import *

class TestArd(unittest.TestCase):
    def setUp(self):
        self.ard=ARDMediathek(None);
        self.assertEqual("ARD", self.ard.name())

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def test_fixTime(self):
        time="10:11:01";
        fixed=self.ard.fixTime(time);
        self.assertEqual("00:11:01", fixed);
        
        time="11:27:24";
        fixed=self.ard.fixTime(time);
        self.assertEqual("01:27:24", fixed);
        
    def test_unescape(self):
        str="Untertitel f&#x00fc;r H&#x00f6;rgesch&#x00e4;digte";
        fixed=self.ard.unescape(str);
        self.assertEqual("Untertitel für Hörgeschädigte", fixed);
        