# 2012 California Election Results Based On SOS

#### How to use this library:

1. Install

    `pip install election`

2. Setup a fake live CA server to test against

    `fake_election_server --delay=0`

3. Pull a copy of NYPR's json data

    `fetch_parse_and_upload_election_data --url=127.0.0.1:2012`

#### How to develop against election_parser 

Election parser comes with tests and a web server that simulates the
CA website on election day.  Please use this data to test against
instead of dropping .xml files randomly into the source repository. 

If you want to make a change to the parser and see the results use the
fetch_parse_and_upload_election_data command as described in step #3
above.


### Source structure

All library code lives in election_parser/* 

All test server code to simulate an election day lives in election_parser/test/* 

Within election_parser:

* loader.GenericLoader: This is a parser mixin class that provides the
  "fetch" method used by all parsers.

* formatter.format: This is a method that will format a python data
  structure to the user's preferred serialization - which serialization
  is determined by the --format command line flag.

* states: This provides State specific parser behavior for each State.
  Currently we're only providing support for California, but its
  becoming obvious what will be generic and what will be state
  specific.  Each class must override GenericParser and a class that
  provides a fetch method with the same interface as GenericLoader.
  If your state is really weird you can provide the fetch method
  inline in the states definition.  The specific requirements for
  these classes are documented in the states docstring and tested for
  in the test_states_meet_requirements module - yes our unittests make
  sure your state is not missing any required fields.

* server.main: This is the meat of the command line tool
  fetch_parse_and_upload_election_data.  Okay, in hindsight "server"
  is a sucky name.  This is changing.

* xml_parser.GenericParser: This provides a generic oasis-open.org
  (http://docs.oasis-open.org/election/510-count-v4-0.xsd) compatible
  parser.  Its really more oasis specific than generic, so if Oasis
  isn't used across all 50 states we'll likely change this classes
  name at some point.



