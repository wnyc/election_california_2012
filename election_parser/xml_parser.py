from StringIO import StringIO 
from lxml.etree import XMLParser,ElementTree
from lxml import etree
import json
import datetime
import decimal

#import xml_parser as a
#open('foo.json','w').write(a.parse({'X12PG_510.xml': open('real/X12PG_510.xml','r')}, 'ca'))

        

class GenericParser:

    def __init__(self, year):
        self.year = int(year)

    def element_tree_factory(self):
        element_tree = ElementTree().parser
        # raise Exception(dir(element_tree))
        #element_tree = XMLParser()
        element_tree.resolvers.add(self.Resolver())
        return element_tree

    def apply_replacements(self, data):
        # I'm sure Knuth knows a faster O(n+m) way of doing this.
        for before, after in self.STRING_REPLACEMENTS:
            data = data.replace(before, after)
        return data
    
    def parse(self, data, update_url=None):
        tree = self.element_tree_factory()
        data = self.read_data(data)
        # data = self.apply_replacements(data)
        # raise Exception(str(type(etree.parse(data, tree))))
        data = data.replace('&nbsp;', '' )
        root = etree.parse(StringIO(data), tree)
        
        data = self.full_parse(root)
        if update_url is not None:
            data['update_url'] = update_url
        yield 'all', data

    def read_data(self, data):
        # We assume there is only one data file, this may not be true
        # for other states, or even for CA - there are multiple files
        # provided by the state and its not certain quite yet that we
        # don't need both of them.
        for filename in data:
            if self.is_correct_file(filename):
                return data[filename].read()

    def full_parse(self, root):
        bodies = {}
        parsed_data_root = {
            "format": ["adapted_sos_1"],
            "bodies": bodies,
            "issuedate" : self.issuedate(root)
            }
        contest_list = self.contests(root)
        for con in contest_list:
            body, condata = self.contest_dict(con)
            key = body[0]
            title = body[1]
            body_dict = bodies.setdefault(key, {'title': title, 'contests':{}})
            contests = body_dict['contests']

            contests[condata['title']] = condata 
        return parsed_data_root

    def issuedate(self, root):
        return root.find("./IssueDate").text

    def candidates(self, contest):
        return contest.findall('./TotalVotes/Selection/Candidate')

    def selections(self, contest):
        return contest.findall('./TotalVotes/Selection')

    def contests(self, root):
        return root.find('./Count/Election/Contests').findall('Contest')

    def vote_tuple(self, selection):
        candidate = selection.find('./Candidate')
        try:
            ballot_name = candidate.find('./CandidateIdentifier/CandidateName').text
            id = candidate.find('./CandidateIdentifier').attrib['Id']
            ballot_measure = False
        except:
            # Ballot Measure
            ballot_measure = True
            ballot_name = candidate.find('./ProposalItem').attrib['ReferendumOptionIdentifier']
            id = ballot_name
        if not ballot_measure:
            last_name = ballot_name.split().pop()
        else:
            last_name = ""
        display_id = '_'.join([last_name.lower(), id])
        votes = int(selection.find('./ValidVotes').text)
        return (display_id, votes)

    def candidate_dict(self, selection):
        ##TODO: issue to group Barack Obama votes across party affils?
        candidate = selection.find('./Candidate')
        try:
            ballot_name = candidate.find('./CandidateIdentifier/CandidateName').text
            id = candidate.find('./CandidateIdentifier').attrib['Id']
            full_party = candidate.find('./Affiliation/Type').text
            party = self.PARTIES.get(full_party, full_party)
            ballot_measure = False
        except AttributeError:
            # Ballot Measure
            ballot_measure = True
            ballot_name = candidate.find('./ProposalItem').attrib['ReferendumOptionIdentifier']
            id = ballot_name
            party = None
        if not ballot_measure:
            last_name = ballot_name.split().pop()
        else:
            last_name = ""
        display_id = '_'.join([last_name.lower(), id])
        votes = int(selection.find('./ValidVotes').text)
        try:
            count_metrics = selection.findall('./CountMetric')
            vote_percent = [x for x in count_metrics if x.attrib['Id']=='PVR'].pop().text
        except:
            vote_percent = None #TODO

        incumbent_field = selection.findall("./AffiliationIdentifier[@Id='Incumbent']")
        if incumbent_field:
            incumbent = True
        else:
            incumbent = False

        return (display_id, {'ballot_name':ballot_name,
            'id': display_id,
            'ballot_name': ballot_name,
            'party': party,
            'last_name':last_name,
            'votes' : votes,
            'incumbent' : incumbent,
            'vote_percent' : vote_percent,
            })

    def precinct_dict(self, precinct):
        total = int(precinct.find('./CountMetric[@Id="TP"]').text)
        reporting = int(precinct.find('./CountMetric[@Id="PR"]').text)
        reporting_percent = 100 * float(reporting)/float(total)
        return {'total': total, 
                'reporting': reporting, 
                'reporting_percent': reporting_percent}


        return state_data[state]['body_mapper'][contest_id[:4]]


    def get_body(self, contest_id):
        return self.BODY_MAPPER[contest_id[:4]]

    def contest_dict(self, contest):
        contest_id = contest.find('./ContestIdentifier').attrib['Id']
        body = self.get_body(contest_id)
        measure_number = self.get_ballot_measure_number(contest_id)
            
        title = contest.find('./ContestIdentifier/ContestName').text
        
        candidates = dict()
        for selection in contest.findall('./TotalVotes/Selection'):
            display_id, candidate = self.candidate_dict(selection)
            candidates[display_id] = candidate

        precincts = self.precinct_dict(contest.find('./TotalVotes'))
        counties = dict()
        geo = dict(state=self.NAME, district=contest_id[6:8])
        for reportingunit in contest.findall('./ReportingUnitVotes'):
            unit_id = reportingunit.find('./ReportingUnitIdentifier').attrib['Id']
            unit_title = reportingunit.find('./ReportingUnitIdentifier').text
            unit_display_id = '_'.join([unit_title, unit_id])

            unit_geo = dict(state=self.NAME, fips=self.FIPS[unit_title])
            unit_geo = dict(unit_geo)
            unit_precincts = self.precinct_dict(reportingunit)
            votes = dict()
            for selection in reportingunit.findall('./Selection'):
                display_id, num_votes = self.vote_tuple(selection)
                votes[display_id] = {'votes':num_votes}
            vote_total = sum([v['votes'] for v in votes.values()])
            for v in votes.values():
                v['vote_percent'] = 100.0*v['votes']/vote_total if vote_total else 0

            counties[unit_display_id] = dict(title=unit_title, 
                                        geo=unit_geo, 
                                        votes=votes, 
                                        precincts=unit_precincts)
        retdict = {
                'contest_id': contest_id,
                'title': title,
                'geo': geo,
                'candidates': candidates,
                'precincts': precincts}
        if measure_number:
            retdict['measure_number'] = measure_number
        if body[0] in self.SHOW_COUNTY_RACES:
            retdict['counties'] = counties

        return (body, retdict)
