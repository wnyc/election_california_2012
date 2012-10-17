from lxml.etree import ElemenTree as ET
import json

STATE = 'ca'

def candidates(contest):
    return contest.findall('./TotalVotes/Selection/Candidate')

def contests(root):
    return root.find('./Count/Election/Contests').findall('Contest')

def votes(selection):
    candidate = selection.find('./Candidate')
    id = candidate.find('./CandidateIdentifier').attrib['Id']
    last_name = ballot_name.split().pop().lower()
    display_id = '_'.join([last_name, id])
    votes = int(selection.find('./ValidVotes').text)
    return (display_id, votes)

def candidate_dict(selection):
    candidate = selection.find('./Candidate')
    ballot_name = candidate.find('./CandidateIdentifier/CandidateName').text
    party = candidate.find('./Affiliation/Type').text
    id = candidate.find('./CandidateIdentifier').attrib['Id']
    last_name = ballot_name.split().pop().lower()
    display_id = '_'.join([last_name, id])
    votes = int(selection.find('./ValidVotes').text)
    vote_percent = [x for x in selection.findall('./CountMetric') if x.attrib['Id']=='PVR'].pop().text
    return (display_id,{'ballot_name':ballot_name,
        'id':id,
        'ballot_name': ballot_name,
        'party':party, 
        'last_name':last_name,
        'votes' : votes,
        'vote_percent' : vote_percent,
        })

def precinct_dict(precinct):
    total = int(precinct.find('./CountMetric[@Id="TP"]').text)
    reporting = int(precinct.find('./CountMetric[@Id="PR"]').text)
    reporting_percent = 100 * float(reporting)/float(total)
    return dict(total=total, reporting=reporting, reporting_percent=reporting_percent)

    
def contest_dict(contest):
    title = contest.find('./ContestIdentifier/ContestName').text
    geo = dict(state=STATE)
    candidates = dict()
    for selection in contest.findall('./TotalVotes/Selection'):
        display_id, candidate = candidate_dict(selection)
        candidates[display_id] = candidates
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
            display_id, num_votes = votes(selection)
            votes[display_id] = num_votes
        counties[display_id] = dict(title=unit_title, geo=geo, votes=votes, precincts=precincts)
    return dict(title=title,
            geo=geo,
            candidates=candidates,
            precincts=precincts,
            counties=counties)

