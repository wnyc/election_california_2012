#!/usr/bin/env python

import election_parser.test
import election_parser.utils
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
        self.json = dict(self.make())

    EXPECTED = 1

    def make(self):
        yield 'all', 1

    def test_does_not_die(self):
        "xml_parser.parse should run without raiseing an exception"
        pass

    def test_parsed_data_is_dict(self):
        "parse should return a dict"
        self.assertTrue(isinstance(self.json, dict))

    def test_parsed_data_as_all_json(self):
        "parse should contain the key all.json"
        self.assertTrue('all' in self.json.keys())

    def test_expected_results(self):
        if self.json['all'] != self.EXPECTED:
            import pprint
            open("/home/adeprince/stuff.py" ,"w+").write(pprint.pformat(self.json['all']))
        self.assertEquals(self.json['all'], self.EXPECTED)

                         


class TestParser(TestTheTestWithoutGoodData):
    def make(self):
        # ZIPFILE is exactly what fetch returns
        parser = election_parser.states.StateParserFactory('ca', 2012)
        return dict(list(parser.parse(self.incoming_data)))
    
    EXPECTED = {'bodies': {'ca.assembly': {'contests': {'State Assembly District 1': {'candidates': {'bosetti_543': {'ballot_name': 'Rick Bosetti',
                                                                                                      'id': 'bosetti_543',
                                                                                                      'last_name': 'Bosetti',
                                                                                                      'party': 'Rep',
                                                                                                      'vote_percent': '58.2',
                                                                                                      'votes': 35174},
                                                                                      'dahle_421': {'ballot_name': 'Brian Dahle',
                                                                                                    'id': 'dahle_421',
                                                                                                    'last_name': 'Dahle',
                                                                                                    'party': 'Rep',
                                                                                                    'vote_percent': '41.8',
                                                                                                    'votes': 25292}},
                                                                       'contest_id': '130000010000',
                                                                       'counties': {'dahle_421': {'geo': {'district': '01',
                                                                                                          'state': 'California'},
                                                                                                  'precincts': {'reporting': 0,
                                                                                                                'reporting_percent': 0.0,
                                                                                                                'total': 60},
                                                                                                  'title': 'Siskiyou',
                                                                                                  'votes': {'bosetti_543': {'vote_percent': 0,
                                                                                                                            'votes': 0},
                                                                                                            'dahle_421': {'vote_percent': 0,
                                                                                                                          'votes': 0}}}},
                                                                       'geo': {'district': '01',
                                                                               'state': 'California'},
                                                                       'precincts': {'reporting': 0,
                                                                                     'reporting_percent': 0.0,
                                                                                     'total': 60},
                                                                       'title': 'State Assembly District 1'}},
                            'title': 'California State Assembly'},
            'ca.propositions': {'contests': {'Temporary Taxes to Fund Education': {'candidates': {'educ._': {'ballot_name': 'Temp Taxes for Educ.',
                                                                                                             'id': 'educ._',
                                                                                                             'last_name': 'Educ.',
                                                                                                             'party': None,
                                                                                                             'vote_percent': None,
                                                                                                             'votes': 1453960}},
                                                                                   'contest_id': '190000000030',
                                                                                   'counties': {'educ._': {'geo': {'district': '00',
                                                                                                                   'state': 'California'},
                                                                                                           'precincts': {'reporting': 7,
                                                                                                                         'reporting_percent': 15.217391304347826,
                                                                                                                         'total': 46},
                                                                                                           'title': 'Yuba',
                                                                                                           'votes': {'educ._': {'vote_percent': 100.0,
                                                                                                                                'votes': 4091}}}},
                                                                                   'geo': {'district': '00',
                                                                                           'state': 'California'},
                                                                                   'precincts': {'reporting': 7,
                                                                                                 'reporting_percent': 15.217391304347826,
                                                                                                 'total': 46},
                                                                                   'title': 'Temporary Taxes to Fund Education'}},
                                'title': 'California Ballot Measures'},
            'ca.senate': {'contests': {'State Senate District 1': {'candidates': {'gaines_96': {'ballot_name': 'Ted Gaines',
                                                                                                'id': 'gaines_96',
                                                                                                'last_name': 'Gaines',
                                                                                                'party': 'Rep',
                                                                                                'vote_percent': '68.3',
                                                                                                'votes': 87562},
                                                                                  'griffith-flatter_355': {'ballot_name': 'Julie Griffith-Flatter',
                                                                                                           'id': 'griffith-flatter_355',
                                                                                                           'last_name': 'Griffith-Flatter',
                                                                                                           'party': 'Dem',
                                                                                                           'vote_percent': '31.7',
                                                                                                           'votes': 40704}},
                                                                   'contest_id': '120000010000',
                                                                   'counties': {'gaines_96': {'geo': {'district': '01',
                                                                                                      'state': 'California'},
                                                                                              'precincts': {'reporting': 0,
                                                                                                            'reporting_percent': 0.0,
                                                                                                            'total': 60},
                                                                                              'title': 'Siskiyou',
                                                                                              'votes': {'gaines_96': {'vote_percent': 0,
                                                                                                                      'votes': 0},
                                                                                                        'griffith-flatter_355': {'vote_percent': 0,
                                                                                                                                 'votes': 0}}}},
                                                                   'geo': {'district': '01',
                                                                           'state': 'California'},
                                                                   'precincts': {'reporting': 0,
                                                                                 'reporting_percent': 0.0,
                                                                                 'total': 60},
                                                                   'title': 'State Senate District 1'}},
                          'title': 'California State Senate'},
            'us.congress': {'contests': {'U.S. House of Representatives District 1': {'candidates': {'malfa_233': {'ballot_name': 'Doug La Malfa',
                                                                                                                   'id': 'malfa_233',
                                                                                                                   'last_name': 'Malfa',
                                                                                                                   'party': 'Rep',
                                                                                                                   'vote_percent': '55.5',
                                                                                                                   'votes': 54772},
                                                                                                     'reed_32': {'ballot_name': 'Jim Reed',
                                                                                                                 'id': 'reed_32',
                                                                                                                 'last_name': 'Reed',
                                                                                                                 'party': 'Dem',
                                                                                                                 'vote_percent': '44.5',
                                                                                                                 'votes': 44001}},
                                                                                      'contest_id': '110000010000',
                                                                                      'counties': {'malfa_233': {'geo': {'district': '01',
                                                                                                                         'state': 'California'},
                                                                                                                 'precincts': {'reporting': 46,
                                                                                                                               'reporting_percent': 100.0,
                                                                                                                               'total': 46},
                                                                                                                 'title': 'Tehama',
                                                                                                                 'votes': {'malfa_233': {'vote_percent': 42.999245386567878,
                                                                                                                                         'votes': 12536},
                                                                                                                           'reed_32': {'vote_percent': 57.000754613432122,
                                                                                                                                       'votes': 16618}}}},
                                                                                      'geo': {'district': '01',
                                                                                              'state': 'California'},
                                                                                      'precincts': {'reporting': 46,
                                                                                                    'reporting_percent': 100.0,
                                                                                                    'total': 46},
                                                                                      'title': 'U.S. House of Representatives District 1'}},
                            'title': 'U.S. Representative in Congress'},
            'us.president': {'contests': {'President': {'candidates': {'barackobama_62': {'ballot_name': 'BarackObama',
                                                                                          'id': 'barackobama_62',
                                                                                          'last_name': 'BarackObama',
                                                                                          'party': 'Dem',
                                                                                          'vote_percent': '48.7',
                                                                                          'votes': 1497922},
                                                                       'garyjohnson_697': {'ballot_name': 'GaryJohnson',
                                                                                           'id': 'garyjohnson_697',
                                                                                           'last_name': 'GaryJohnson',
                                                                                           'party': 'Lib',
                                                                                           'vote_percent': '1.9',
                                                                                           'votes': 57975},
                                                                       'jillstein_22': {'ballot_name': 'JillStein',
                                                                                        'id': 'jillstein_22',
                                                                                        'last_name': 'JillStein',
                                                                                        'party': 'Grn',
                                                                                        'vote_percent': '5.0',
                                                                                        'votes': 152639},
                                                                       'mittromney_23': {'ballot_name': 'MittRomney',
                                                                                         'id': 'mittromney_23',
                                                                                         'last_name': 'MittRomney',
                                                                                         'party': 'Rep',
                                                                                         'vote_percent': '20.6',
                                                                                         'votes': 633737},
                                                                       'roseannebarr_696': {'ballot_name': 'RoseanneBarr',
                                                                                            'id': 'roseannebarr_696',
                                                                                            'last_name': 'RoseanneBarr',
                                                                                            'party': 'PFP',
                                                                                            'vote_percent': '3.1',
                                                                                            'votes': 96652},
                                                                       'thomashoefling_695': {'ballot_name': 'ThomasHoefling',
                                                                                              'id': 'thomashoefling_695',
                                                                                              'last_name': 'ThomasHoefling',
                                                                                              'party': 'Ind',
                                                                                              'vote_percent': '20.7',
                                                                                              'votes': 636733}},
                                                        'contest_id': '010000000000',
                                                        'counties': {'roseannebarr_696': {'geo': {'district': '00',
                                                                                                  'state': 'California'},
                                                                                          'precincts': {'reporting': 7,
                                                                                                        'reporting_percent': 15.217391304347826,
                                                                                                        'total': 46},
                                                                                          'title': 'Yuba',
                                                                                          'votes': {'barackobama_62': {'vote_percent': 4.5726102941176467,
                                                                                                                       'votes': 199},
                                                                                                    'garyjohnson_697': {'vote_percent': 1.9301470588235294,
                                                                                                                        'votes': 84},
                                                                                                    'jillstein_22': {'vote_percent': 24.816176470588236,
                                                                                                                     'votes': 1080},
                                                                                                    'mittromney_23': {'vote_percent': 41.222426470588232,
                                                                                                                      'votes': 1794},
                                                                                                    'roseannebarr_696': {'vote_percent': 0.45955882352941174,
                                                                                                                         'votes': 20},
                                                                                                    'thomashoefling_695': {'vote_percent': 26.999080882352942,
                                                                                                                           'votes': 1175}}}},
                                                        'geo': {'district': '00',
                                                                'state': 'California'},
                                                        'precincts': {'reporting': 7,
                                                                      'reporting_percent': 15.217391304347826,
                                                                      'total': 46},
                                                        'title': 'President'}},
                             'title': 'U.S. President'},
            'us.senate': {'contests': {'U.S. Senate': {'candidates': {'diannefeinstein_173': {'ballot_name': 'DianneFeinstein',
                                                                                              'id': 'diannefeinstein_173',
                                                                                              'last_name': 'DianneFeinstein',
                                                                                              'party': 'Dem',
                                                                                              'vote_percent': '51.5',
                                                                                              'votes': 1577017},
                                                                      'elizabethemken_396': {'ballot_name': 'ElizabethEmken',
                                                                                             'id': 'elizabethemken_396',
                                                                                             'last_name': 'ElizabethEmken',
                                                                                             'party': 'Rep',
                                                                                             'vote_percent': '48.5',
                                                                                             'votes': 1484516}},
                                                       'contest_id': '100000000001',
                                                       'counties': {'elizabethemken_396': {'geo': {'district': '00',
                                                                                                   'state': 'California'},
                                                                                           'precincts': {'reporting': 7,
                                                                                                         'reporting_percent': 15.217391304347826,
                                                                                                         'total': 46},
                                                                                           'title': 'Yuba',
                                                                                           'votes': {'diannefeinstein_173': {'vote_percent': 1.9990808823529411,
                                                                                                                             'votes': 87},
                                                                                                     'elizabethemken_396': {'vote_percent': 98.000919117647058,
                                                                                                                            'votes': 4265}}}},
                                                       'geo': {'district': '00',
                                                               'state': 'California'},
                                                       'precincts': {'reporting': 7,
                                                                     'reporting_percent': 15.217391304347826,
                                                                     'total': 46},
                                                       'title': 'U.S. Senate'}},
                          'title': 'U.S. Senate'}},
 'format': ['adapted_sos_1']}
