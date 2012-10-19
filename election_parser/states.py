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
    FIPS = {
        "Alameda":"06001",
        "Alpine":"06003",
        "Amador":"06005",
        "Butte":"06007",
        "Calaveras":"06009",
        "Colusa":"06011",
        "Contra Costa":"06013",
        "Del Norte":"06015",
        "El Dorado":"06017",
        "Fresno":"06019",
        "Glenn":"06021",
        "Humboldt":"06023",
        "Imperial":"06025",
        "Inyo":"06027",
        "Kern":"06029",
        "Kings":"06031",
        "Lake":"06033",
        "Lassen":"06035",
        "Los Angeles":"06037",
        "Madera":"06039",
        "Marin":"06041",
        "Mariposa":"06043",
        "Mendocino":"06045",
        "Merced":"06047",
        "Modoc":"06049",
        "Mono":"06051",
        "Monterey":"06053",
        "Napa":"06055",
        "Nevada":"06057",
        "Orange":"06059",
        "Placer":"06061",
        "Plumas":"06063",
        "Riverside":"06065",
        "Sacramento":"06067",
        "San Benito":"06069",
        "San Bernardino":"06071",
        "San Diego":"06073",
        "San Francisco":"06075",
        "San Joaquin":"06077",
        "San Luis Obispo":"06079",
        "San Mateo":"06081",
        "Santa Barbara":"06083",
        "Santa Clara":"06085",
        "Santa Cruz":"06087",
        "Shasta":"06089",
        "Sierra":"06091",
        "Siskiyou":"06093",
        "Solano":"06095",
        "Sonoma":"06097",
        "Stanislaus":"06099",
        "Sutter":"06101",
        "Tehama":"06103",
        "Trinity":"06105",
        "Tulare":"06107",
        "Tuolumne":"06109",
        "Ventura":"06111",
        "Yolo":"06113",
        "Yuba":"06115"

    }
    BODY_MAPPER = {
        '0100': ["us.president", "U.S. President"],
        '1000': ["us.senate", "U.S. Senate"],
        '1100': ["us.house", "U.S. Representative in Congress"],
        '1200': ["ca.senate", "California State Senate"],
        '1300': ["ca.assembly", "California State Assembly"],
        '1900': ["ca.propositions", "California Ballot Measures"]
        }
    NAME = "CA"
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

