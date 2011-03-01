#!/usr/bin/env python
"""
Filter JSON in sys.stdin to find only docs that match each regex against raw JSON.

e.g.

    zcat allposts.20100818.json.gz | ~/dev/common-scripts/filter-json.py "morgan.*stanley"

Command line parameters = regexes (case-insensitive).
"""

import sys
assert len(sys.argv) > 1

import re
allre = [re.compile(arg, re.I) for arg in sys.argv[1:]]
#for arg in sys.argv[1:]: print arg

import common.json
from common.str import percent
keptdocs = []
alldocs = common.json.load(sys.stdin)
for doc in alldocs:
    docjson = common.json.dumps(doc)
    missedone_regex = False
    for r in allre:
        if not r.search(docjson):
            missedone_regex = True
            break
    if missedone_regex: continue
    keptdocs.append(doc)

print >> sys.stderr, "Kept %s documents with regexs: %s" % (percent(len(keptdocs), len(alldocs)), `allre`)

common.json.dump(keptdocs, sys.stdout, indent=4)
