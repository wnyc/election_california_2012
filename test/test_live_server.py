#!/usr/bin/env python

import unittest
import election_parser.test.live_server 

class TestTimeSensitiveFileLookup(unittest.TestCase):
    def setUp(self):
        self.tsfl = election_parser.test.live_server.TimeSensitiveFileLookup(
            ("0-index.html", "1-index.html", "2-index.html"), 60)
        
    def test_0(self):
        self.assertEquals(self.tsfl.get('index.html', 0),
                          '0-index.html')
    def test_59(self):
        self.assertEquals(self.tsfl.get('index.html', 59),
                          '0-index.html')
    def test_60(self):
        self.assertEquals(self.tsfl.get('index.html', 60),
                          '1-index.html')
    def test_61(self):
        self.assertEquals(self.tsfl.get('index.html', 61),
                          '1-index.html')
    def test_119(self):
        self.assertEquals(self.tsfl.get('index.html', 119),
                          '1-index.html')
    def test_120(self):
        self.assertEquals(self.tsfl.get('index.html', 120),
                          '2-index.html')
    def test_12345678(self):
        self.assertEquals(self.tsfl.get('index.html', 12345678),
                          '2-index.html')
    def test_minus_12345678(self):
        self.assertEquals(self.tsfl.get('index.html', -12345678),
                          '0-index.html')
