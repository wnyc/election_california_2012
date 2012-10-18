from lxml.etree import ElementTree as ET
from lxml import etree
import json
import datetime
import decimal

from states import data as state_data

#import xml_parser as a
#open('foo.json','w').write(a.parse({'X12PG_510.xml': open('real/X12PG_510.xml','r')}, 'ca'))

def parse(data, state):
    e = ET()
    xmlhandle = e.parse(data[state_data[state]['file']])
    return json.dumps(full_parse(xmlhandle, state))

def full_parse(root, state):
    rv = {
        "format": ["adapted_sos_1"],
        "last_updated": str(datetime.datetime.now()),
        "bodies": {}
        }
    contest_list = contests(root)
    for con in contest_list:
        body, condata = contest_dict(con, state)
        rv['bodies'].setdefault(body[0], {'title': body[1], 'contests':{}})
        rv['bodies'][body[0]]['contests'][condata['title']] = condata
    return rv

def candidates(contest):
    return contest.findall('./TotalVotes/Selection/Candidate')

def selections(contest):
    return contest.findall('./TotalVotes/Selection')

def contests(root):
    return root.find('./Count/Election/Contests').findall('Contest')

def vote_tuple(selection):
    candidate = selection.find('./Candidate')
    try:
        ballot_name = candidate.find('./CandidateIdentifier/CandidateName').text
        id = candidate.find('./CandidateIdentifier').attrib['Id']
    except:
        ballot_name = candidate.find('./ProposalItem').attrib['ProposalIdentifier']
        id = ''
    last_name = ballot_name.split().pop()
    display_id = '_'.join([last_name.lower(), id])
    votes = int(selection.find('./ValidVotes').text)
    return (display_id, votes)

def candidate_dict(selection, state):
    ##TODO: issue to group Barack Obama votes across party affils?
    candidate = selection.find('./Candidate')
    try:
        ballot_name = candidate.find('./CandidateIdentifier/CandidateName').text
        id = candidate.find('./CandidateIdentifier').attrib['Id']
        full_party = candidate.find('./Affiliation/Type').text
        party = state_data[state]['parties'].get(full_party, full_party)
    except AttributeError:
        ballot_name = candidate.find('./ProposalItem').attrib['ProposalIdentifier']
        id = ''
        party = None
    last_name = ballot_name.split().pop()
    display_id = '_'.join([last_name.lower(), id])
    votes = int(selection.find('./ValidVotes').text)
    try:
        count_metrics = selection.findall('./CountMetric')
        vote_percent = [x for x in count_metrics if x.attrib['Id']=='PVR'].pop().text
    except:
        vote_percent = None #TODO

    return (display_id, {'ballot_name':ballot_name,
        'id': display_id,
        'ballot_name': ballot_name,
        'party': party,
        'last_name':last_name,
        'votes' : votes,
        'vote_percent' : vote_percent,
        })

def precinct_dict(precinct):
    total = int(precinct.find('./CountMetric[@Id="TP"]').text)
    reporting = int(precinct.find('./CountMetric[@Id="PR"]').text)
    reporting_percent = 100 * float(reporting)/float(total)
    return {'total': total, 
            'reporting': reporting, 
            'reporting_percent': reporting_percent}


def get_body(state, contest_id):
    return state_data[state]['body_mapper'][contest_id[:4]]
    
def contest_dict(contest, state):
    contest_id = contest.find('./ContestIdentifier').attrib['Id']
    body = get_body(state, contest_id)
    title = contest.find('./ContestIdentifier/ContestName').text
    geo = dict(state=state, district=contest_id[6:8])
    candidates = dict()
    for selection in contest.findall('./TotalVotes/Selection'):
        display_id, candidate = candidate_dict(selection, state)
        candidates[display_id] = candidate

    precincts = precinct_dict(contest.find('./TotalVotes'))
    counties = dict()
    for reportingunit in contest.findall('./ReportingUnitVotes'):
        unit_id = reportingunit.find('./ReportingUnitIdentifier').attrib['Id']
        unit_title = reportingunit.find('./ReportingUnitIdentifier').text
        display_id = '_'.join([unit_title, unit_id])
        report_geo = dict(geo)
        precincts = precinct_dict(reportingunit)
        votes = dict()
        for selection in reportingunit.findall('./Selection'):
            display_id, num_votes = vote_tuple(selection)
            votes[display_id] = {'votes':num_votes}
        vote_total = sum([v['votes'] for v in votes.values()])
        for v in votes.values():
            v['vote_percent'] = 100.0*v['votes']/vote_total if vote_total else 0
        
        counties[display_id] = dict(title=unit_title, 
                                    geo=report_geo, 
                                    votes=votes, 
                                    precincts=precincts)
    return (body, {
            'contest_id': contest_id,
            'title': title,
            'geo': geo,
            'candidates': candidates,
            'precincts': precincts,
            'counties': counties})
