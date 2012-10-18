import unittest
import election_parser.states
import sys
from lxml import etree 


this = sys.modules[__name__]


class CheckFields:
    def assertHas(self, attr):
        self.assertTrue(hasattr(self.klass, attr))

    def test_has_name(self):
        self.assertHas('NAME')

    def test_body_mapper(self):
        self.assertHas('BODY_MAPPER')
    
    def test_fetch(self):
        self.assertHas('fetch')
    
    def test_parties(self):
        self.assertHas('PARTIES')
    
    def test_has_is_correct_file(self):
        self.assertHas('is_correct_file')
    
    def test_URL(self):
        self.assertHas('URL')
    
    def test_Resolver(self):
        self.assertHas('Resolver')

    def test_resolver_is_a_resolver(self):
        self.assertTrue(issubclass(self.klass.Resolver, etree.Resolver))

    def test_is_listed(self):
        self.assertTrue(self.klass in election_parser.states.PARSER_CLASSES.values())

    def test_reactable_by_factory(self):
        for key, klass in election_parser.states.PARSER_CLASSES.items():
            if klass == self.klass:
                break
            key = None
        self.assertTrue(key is not None)
        self.assertTrue(isinstance(election_parser.states.StateParserFactory(key, '2012'), klass))
    
class SampleClass:
    pass

aclass = type(SampleClass)

for state in dir(election_parser.states):

    state = getattr(election_parser.states, state)
    # raise Exception(type(state))
    if isinstance(state, aclass) and issubclass(state, election_parser.xml_parser.GenericParser) and not issubclass(election_parser.xml_parser.GenericParser, state):
        # We need to create a test for this
        name = str(state).split('.')[-1]
        name = "Test%s" % (name,)
        setattr(this, name, type(name, (unittest.TestCase, CheckFields), {'klass':state}))


    
