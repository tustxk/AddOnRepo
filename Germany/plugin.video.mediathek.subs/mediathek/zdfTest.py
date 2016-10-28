# coding=utf-8
import unittest
from mediathek.zdf import *
from simplexbmcMock import SimpleXbmcGui

class TestZdf(unittest.TestCase):
    def setUp(self):
        self.zdf=ZDFMediathek(SimpleXbmcGui());
        self.assertEqual("ZDF", self.zdf.name())

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def test_fixTime(self):
        time="59";
        fixed=self.zdf.fixTime(time);
        self.assertEqual("00:00:59", fixed);
        
        time="360";
        fixed=self.zdf.fixTime(time);
        self.assertEqual("00:06:00", fixed);
        
        time="600";
        fixed=self.zdf.fixTime(time);
        self.assertEqual("00:10:00", fixed);
        
        time="3600";
        fixed=self.zdf.fixTime(time);
        self.assertEqual("01:00:00", fixed);
        
        time="4242";
        fixed=self.zdf.fixTime(time);
        self.assertEqual("01:10:42", fixed);