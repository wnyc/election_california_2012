#!/usr/bin/env python

import election_parser.test
import election_parser.utils
from pkg_resources import resource_filename
import unittest

ZIPFILE = resource_filename(election_parser.test.__name__, 'data/00000001-X12PG.zip')

class TestZipDict(unittest.TestCase):
    def setUp(self):
        self.zf = election_parser.utils.ZipDict(ZIPFILE)

    def test_keys(self):
        self.assertEquals(sorted(self.zf.keys()),
                          sorted(['X12PG_530.xml', 'X12PG_510.xml', 'X12PG_510_0100.xml', 'X12PG_510_1000.xml', 'X12PG_510_1100.xml', 'X12PG_510_1200.xml', 'X12PG_510_1300.xml', 'X12PG_510_1900.xml']))

    def test_raises_key_error(self):
        self.assertRaises(KeyError,
                          lambda: self.zf['sdfsdfs'])

    def test_returns_default(self):
        self.assertEquals('1234',
                          self.zf.get('foobar', '1234'))
    
    def test_retuns_fileobject(self):
        self.assertEquals(self.zf['X12PG_530.xml'].readline(),
                          '<EML Id="530" SchemaVersion="5.0">\n')

    def test_retuns_fileobject(self):
        self.assertEquals(self.zf.get('X12PG_530.xml').readline(),
                          '<EML Id="530" SchemaVersion="5.0">\n')
