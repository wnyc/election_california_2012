from election_parser.exceptions import UnknownState
from election_parser.xml_parser import GenericParser


class California(GenericParser):
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

    def is_correct_file(self, filename):
        return self.year == "2012" and filename == "X12PG_510.xml"

    
def StateParserFactory(state, year):
    # Eventually we might need different classes for different years.
    parser_class = {'ca':California}.get(state.lower())
    if not parser_class:
        raise UnknownState(state)
    return parse_class(year)

