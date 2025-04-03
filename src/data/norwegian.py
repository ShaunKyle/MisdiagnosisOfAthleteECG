# Utility functions for extracting labels from:
# - Norwegian endurance athlete dataset (Single line cardiologist report)

from typing import List
from enum import Enum

# Parsing single-line cardiologist reports
# ----------------------------------------

def extract_findings(report: str, follow_on: bool=True, split_and=True) -> List[str]:
    """Extract a list of all findings in a single line cardiologist report
    """
    comments = report.split(': ', maxsplit=1)[1].split(', ')
    
    # Also split multiple findings in a single comment joined by 'and'.
    # e.g. Sinus bradycardia and sinus arrhythmia and first degree AV block
    if split_and:
        temp = []
        for comment in comments:
            for segment in comment.split('and'):
                temp.append(segment)
        comments = temp

    # Cleanup (e.g. remove leading/trailing whitespace)
    comments[:] = list(map(str.strip, comments))

    if not follow_on:
        return comments     # i.e. assume every comment is a new finding

    # Combine follow-on comments with parent comment to produce full finding 
    # for SL12 machine comments.
    #
    # e.g. ST elevation, consider early repolarization, pericarditis, or injury
    findings = []
    for i, comment in enumerate(comments):
        if comment[0].isupper() or comment[0] == '*':
            findings.append(comment)
        else:
            findings[-1] = ''.join([findings[-1], ", ", comment])
    return findings


# Labels
# ------

def classify_relevant_findings(comments: List[int]):
    """Returns a list of SNOMED-CT diagnosis codes.

    Only works with norwegian-athlete-ecg dataset and extract_findings.
    """
    findings = []
    
    for c in comments:
        c = c.lower()
        # Sinus rhythm
        if c.find("sinus") != -1:
            if c.find("arrhythmia") != -1:
                findings.append(427393009)
            if c.find("bradycardia") != -1:
                findings.append(426177001)
            if c.find("tachycardia") != -1:
                findings.append(427084000)
            if (c.find("normal") != -1) and not (c.find("abnormal") != -1):
                findings.append(426783006)
    
        # Right bundle branch block
        if c.find("right bundle branch block") != -1:
            if c.find("incomplete") != -1:
                findings.append(713426002)
            elif c.find("complete") != -1:
                findings.append(713427006)

        # T-wave

    return findings


class OverallFinding(Enum):
    Unknown = -99
    Normal = 0
    Borderline = 1
    Abnormal = 2

def classifyOverallFinding(findings: List[str]) -> OverallFinding:
    """Classifies the overall finding for an ECG recording.

    Assumes that the final finding in `findings` list comments on overall 
    finding.
    """
    overall = findings[-1].lower()
    if overall.find("abnormal") != -1:
        return OverallFinding.Abnormal
    elif overall.find("borderline") != -1:
        return OverallFinding.Borderline
    elif overall.find("normal") != -1:
        return OverallFinding.Normal
    else:
        return OverallFinding.Unknown
