from lxml.etree import ElementTree as ET
from lxml import etree
import json
import datetime

STATE = 'ca'
e = ET().parse(open('real/X12PG_510.xml', 'r'))
def full_parse(root):
    rv = {
        "format": ["adapted_sos_1"],
        "last_updated": str(datetime.datetime.now()),
        "bodies": {}
        }
    contest_list = contests(root)
    for con in contest_list:
        condata = contest_dict(con)
        rv[condata['title']] = contest_dict(con)
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
    last_name = ballot_name.split().pop().lower()
    display_id = '_'.join([last_name, id])
    votes = int(selection.find('./ValidVotes').text)
    return (display_id, votes)

def candidate_dict(selection):
    candidate = selection.find('./Candidate')
    try:
        ballot_name = candidate.find('./CandidateIdentifier/CandidateName').text
        id = candidate.find('./CandidateIdentifier').attrib['Id']
        party = candidate.find('./Affiliation/Type').text
    except:
        ballot_name = candidate.find('./ProposalItem').attrib['ProposalIdentifier']
        id = ''
        party = None
    last_name = ballot_name.split().pop().lower()
    display_id = '_'.join([last_name, id])
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

    
def contest_dict(contest):
    title = contest.find('./ContestIdentifier/ContestName').text
    geo = dict(state=STATE)
    candidates = dict()
    for selection in contest.findall('./TotalVotes/Selection'):
        display_id, candidate = candidate_dict(selection)
        candidates[display_id] = candidate

    precincts = precinct_dict(contest.find('./TotalVotes'))
    counties = dict()
    for reportingunit in contest.findall('./ReportingUnitVotes'):
        unit_id = reportingunit.find('./ReportingUnitIdentifier').attrib['Id']
        unit_title = reportingunit.find('./ReportingUnitIdentifier').text
        display_id = '_'.join([unit_title, unit_id])
        geo = dict(state=STATE)
        precincts = precinct_dict(reportingunit)
        votes = dict()
        for selection in reportingunit.findall('./Selection'):
            display_id, num_votes = vote_tuple(selection)
            votes[display_id] = num_votes
        counties[display_id] = dict(title=unit_title, geo=dict(geo), votes=votes, precincts=precincts)
    return {'title': title,
            'geo': geo,
            'candidates': candidates,
            'precincts': precincts,
            'counties': counties}

