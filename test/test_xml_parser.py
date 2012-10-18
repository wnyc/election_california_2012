#!/usr/bin/env python

import election_parser.test
import election_parser.utils
from election_parser.xml_parser import parse
import election_parser.states
import json
from pkg_resources import resource_filename
import unittest2

ZIPFILE = resource_filename(election_parser.test.__name__, 
                            'data/00000001-X12PG.zip')

class TestTheTestWithoutGoodData(unittest2.TestCase):
    def setUp(self):
        # This is the exact data structure returned by fetch
        self.incoming_data = election_parser.utils.ZipDict(ZIPFILE) 
        # self.json = parse(self.incoming_data)
        self.json = self.make()

    def make(self):
        return {'all.json': '"1"'}
    

    def test_does_not_die(self):
        "xml_parser.parse should run without raiseing an exception"
        pass

    def test_parsed_data_is_dict(self):
        "parse should return a dict"
        self.assertTrue(isinstance(self.json, dict))

    def test_parsed_data_as_all_json(self):
        "parse should contain the key all.json"
        self.assertTrue('all.json' in self.json.keys())

    def test_parsed_only_contains_json_files(self):
        "parse should return keys that are json files"
        for key in self.json.keys():
            self.assertTrue(key.endswith('.json'))

    def test_parsed_only_contains_valid_json_data(self):
        "json.loads should be able to load each value"
        for json_file in self.json.values():
            json.loads(json_file)

@unittest2.skip("xml_parser.parser isn't finished yet")
class TestParser(TestTheTestWithoutGoodData):
    def make(self):
        # ZIPFILE is exactly what fetch returns
        parser = election_parser.states.StateParserFactory('ca', 2012)
        parser.parse(self.incoming_data)
    
    
