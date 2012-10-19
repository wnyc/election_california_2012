from lxml import etree 
from election_parser.exceptions import UnknownState

from election_parser.xml_parser import GenericParser
from election_parser.loader import GenericLoader
from pkg_resources import resource_filename

class California(GenericParser, GenericLoader):

    PARTIES = {
        'Democratic': "Dem",
        'Republican': "Rep",
        'American Independent': "Ind",
        'Green': "Grn",
        'Libertarian': "Lib",
        'Peace and Freedom': "PFP",
        'Americans Elect': "AE",
        'No Party Preference': "",
        }
    BODY_MAPPER = {
        '0100': ["us.president", "U.S. President"],
        '1000': ["us.senate", "U.S. Senate"],
        '1100': ["us.congress", "U.S. Representative in Congress"],
        '1200': ["ca.senate", "California State Senate"],
        '1300': ["ca.assembly", "California State Assembly"],
        '1900': ["ca.propositions", "California Ballot Measures"]
        }
    NAME = "California"
    STRING_REPLACEMENTS = (('&nbsp;', '&#160;'),)

    def is_correct_file(self, filename):
        return self.year == 2012 and filename.startswith("X12PG_510.xml")

    def get_ballot_measure_number(self, contestid):
        if contestid.startswith("1900"):
            return contestid[-5:]
        return ''

    URL = "http://media.sos.ca.gov/media/X12PG.zip"

    class Resolver(etree.Resolver):
        def resolve(self, url, pubid, context):
            return self.resolve_filename(resource_filename(__name__, 'xsd/510-count-v4-0.xsd'), context)
        
        
PARSER_CLASSES = {'ca':California}
STATE_ABBREVIATIONS = sorted(PARSER_CLASSES.keys())
YEARS = ['2012']
def StateParserFactory(state, year):
    # Eventually we might need different classes for different years.
    parser_class = PARSER_CLASSES.get(state.lower())
    if not parser_class:
        raise UnknownState(state)
    return parser_class(year)

