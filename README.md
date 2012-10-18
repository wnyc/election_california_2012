# 2012 California Election Results Based On SOS

#### How to use this library:

1. Install

    `pip install election`

2. Setup a fake live CA server to test against

    `fake_election_server --delay=0`

3. Talk to the server

    `python`

4. In python shell, run:

````
Python version 2.6.1
>>> import election.ca

# If this was a real election you'd just write "election.ca.fetch()"
>>> data = election.ca.fetch(url='127.0.0.1:2012')  

>>> data.keys()
['X12PG_530.xml', 'X12PG_510.xml', 'X12PG_510_0100.xml', 'X12PG_510_1000.xml',
'X12PG_510_1100.xml', 'X12PG_510_1200.xml', 'X12PG_510_1300.xml', 'X12PG_510_19
````
