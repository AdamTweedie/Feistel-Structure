"""
Template file for ECMM462 coursework

Academic Year: 2022/23
Version: 2
Author: Diego Marmsoler
"""
import sys
import re

# Alice
rightsalice = {}
alicemaxprio = ''
alicemaxcat = []
alicecurrentprio = ''
alicecurrentcat = []

file1 = open('alice.txt', 'r')
lines = file1.readlines()
if (len(lines) != 3):
    raise SystemExit("Wrong file format")

c = re.compile('^([wra]?),([wra]?),([wra]?)$')
result = c.search(lines[0])
if (not result):
    raise SystemExit("Wrong file format")
rightsalice[1] = result.group(1)
rightsalice[2] = result.group(2)
rightsalice[3] = result.group(3)

prio = lines[1].strip().split(":")
if (len(prio) != 2):
    raise SystemExit("Wrong file format")

if (prio[0] == 'h' or prio[0] == 'l'):
    alicemaxprio = prio[0]
else:
    raise SystemExit("Wrong file format")

cat = prio[1].split(",")
for c in cat:
    if (c == 'A' or c == 'B' or c == 'C'):
        alicemaxcat.append(c)

prio = lines[2].strip().split(":")
if (len(prio) != 2):
    raise SystemExit("Wrong file format")

if (prio[0] == 'h' or prio[0] == 'l'):
    alicecurrentprio = prio[0]
else:
    raise SystemExit("Wrong file format")

cat = prio[1].split(",")
for c in cat:
    if (c == 'A' or c == 'B' or c == 'C'):
        alicecurrentcat.append(c)

# Bob
rightsbob = {}
bobmaxprio = ''
bobmaxcat = []
bobcurrentprio = ''
bobcurrentcat = []

file1 = open('bob.txt', 'r')
lines = file1.readlines()
if (len(lines) != 3):
    raise SystemExit("Wrong file format")

c = re.compile('^([wra]?),([wra]?),([wra]?)$')
result = c.search(lines[0])
if (not result):
    raise SystemExit("Wrong file format")
rightsbob[1] = result.group(1)
rightsbob[2] = result.group(2)
rightsbob[3] = result.group(3)

prio = lines[1].strip().split(":")
if (len(prio) != 2):
    raise SystemExit("Wrong file format")

if (prio[0] == 'h' or prio[0] == 'l'):
    bobmaxprio = prio[0]
else:
    raise SystemExit("Wrong file format")

cat = prio[1].split(",")
for c in cat:
    if (c == 'A' or c == 'B' or c == 'C'):
        bobmaxcat.append(c)

prio = lines[2].strip().split(":")
if (len(prio) != 2):
    raise SystemExit("Wrong file format")

if (prio[0] == 'h' or prio[0] == 'l'):
    bobcurrentprio = prio[0]
else:
    raise SystemExit("Wrong file format")

cat = prio[1].split(",")
for c in cat:
    if (c == 'A' or c == 'B' or c == 'C'):
        bobcurrentcat.append(c)

# Charlie
rightscharlie = {}
charliemaxprio = ''
charliemaxcat = []
charliecurrentprio = ''
charliecurrentcat = []

file1 = open('charlie.txt', 'r')
lines = file1.readlines()
if len(lines) != 3:
    raise SystemExit("Wrong file format")

c = re.compile('^([wra]?),([wra]?),([wra]?)$')
result = c.search(lines[0])
if (not result):
    raise SystemExit("Wrong file format")
rightscharlie[1] = result.group(1)
rightscharlie[2] = result.group(2)
rightscharlie[3] = result.group(3)

prio = lines[1].strip().split(":")
if (len(prio) != 2):
    raise SystemExit("Wrong file format")

if (prio[0] == 'h' or prio[0] == 'l'):
    charliemaxprio = prio[0]
else:
    raise SystemExit("Wrong file format")

cat = prio[1].split(",")
for c in cat:
    if (c == 'A' or c == 'B' or c == 'C'):
        charliemaxcat.append(c)

prio = lines[2].strip().split(":")
if (len(prio) != 2):
    raise SystemExit("Wrong file format")

if (prio[0] == 'h' or prio[0] == 'l'):
    charliecurrentprio = prio[0]
else:
    raise SystemExit("Wrong file format")

cat = prio[1].split(",")
for c in cat:
    if (c == 'A' or c == 'B' or c == 'C'):
        charliecurrentcat.append(c)


# MAIN

def ssc(alice, bob, charlie):
    # Implement check for simple security condition

    subject_results = []
    subjects = [alice, bob, charlie]
    max_prios = [alicemaxprio, bobmaxprio, charliemaxprio]
    max_cats = [alicemaxcat, bobmaxcat, charliemaxcat]

    for subject, max_prio, max_cat in zip(subjects, max_prios, max_cats):
        if len(subject) != 0:
            valid = False
            doc = list(subject.keys())[0]
            action = list(subject.values())[0]
            if action in ('e', 'a'):  # cannot read
                valid = True
            if action == 'r' or action == 'w':
                # s dom o
                if sec_int(get_required_sec_level(doc)) <= sec_int(max_prio):
                    if all(x in max_cat for x in get_required_sec_cat(doc)):
                        if valid:  # if and only if
                            valid = False
                        else:
                            valid = True
            subject_results.append(valid)

    return all(subject_results)


def star(alice, bob, charlie):
    # Implement check for star property

    star_results = []
    subjects = [alice, bob, charlie]
    current_prio = [alicecurrentprio, bobcurrentprio, charliecurrentprio]
    current_cat = [alicecurrentcat, bobcurrentcat, charliecurrentcat]

    for subject, cur_prio, cur_cat in zip(subjects, current_prio, current_cat):
        if len(subject) != 0:
            doc = list(subject.keys())[0]
            p = list(subject.values())[0]
            if p == 'a':
                # f(o) dom fc(s)
                if sec_int(cur_prio) <= sec_int(get_required_sec_level(doc)):
                    if all(x in get_required_sec_cat(doc) for x in cur_cat):
                        star_results.append(True)
                    else:
                        star_results.append(False)
            elif p == 'r':
                # fc(s) dom f(o)
                if sec_int(get_required_sec_level(doc)) <= sec_int(cur_prio):
                    if all(x in cur_cat for x in get_required_sec_cat(doc)):
                        star_results.append(True)
                    else:
                        star_results.append(False)
            elif p == 'w':
                # f(o) = fc(s)
                if (get_required_sec_level(doc) == prio) and (get_required_sec_cat(doc) == cat):
                    star_results.append(True)
                else:
                    star_results.append(False)

    return all(star_results)


def ds(alice, bob, charlie):
    # Implement check for discretionary security condition

    subjects = [alice, bob, charlie]
    subject_rights = [rightsalice, rightsbob, rightscharlie]
    ds_results = []
    for subject, rights in zip(subjects, subject_rights):
        if len(subject) != 0:
            doc = list(subject.keys())[0]
            p = list(subject.values())[0]

            if p == rights[int(doc)]:
                ds_results.append(True)
            else:
                ds_results.append(False)

    return all(ds_results)


def get_required_sec_level(doc):
    # Get security level for each document
    doc_sec_levels = {
        "1": "l",
        "2": "h",
        "3": "h"
    }
    return doc_sec_levels[doc]


def get_required_sec_cat(doc):
    # get security category for each document
    doc_sec_cat = {
        "1": ["A", "B"],
        "2": ["C"],
        "3": ["B"]
    }
    return doc_sec_cat[doc]


def sec_int(rating):
    # convert the security level to integer
    return 1 if rating == "l" else 2


alice = {}
bob = {}
charlie = {}
c = re.compile('^([ABC]):([123]):([rwa])$')
args = sys.argv[1:]
while (len(args) > 0):
    input = args.pop(0)
    result = c.search(input)
    if (not result):
        raise SystemExit("Usage: blpcheck.py [ABC]:[123]:[rwa] ...")
    if (result.group(1) == 'A'):
        if result.group(2) in alice:
            raise SystemExit("duplicate entry")
        alice[result.group(2)] = result.group(3)
    if (result.group(1) == 'B'):
        if result.group(2) in bob:
            raise SystemExit("duplicate entry")
        bob[result.group(2)] = result.group(3)
    if (result.group(1) == 'C'):
        if result.group(2) in charlie:
            raise SystemExit("duplicate entry")
        charlie[result.group(2)] = result.group(3)

print("SSC: ", "Yes" if ssc(alice, bob, charlie) else "No")
print("Star: ", "Yes" if star(alice, bob, charlie) else "No")
print("DS: ", "Yes" if ds(alice, bob, charlie) else "No")
