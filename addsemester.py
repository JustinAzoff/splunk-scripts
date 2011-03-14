#!/usr/bin/env python
"""
Add semester - Add a semester field, so you can do
| addsemester | stats max(clients) by semester
"""

import sys,splunk.Intersplunk
import datetime
import time

def get_semester(d):
    year = d.year
    month = d.month
    day = d.day

    if month < 5 or (month==5 and day<=15):
        return "Spring %d" % year
    if month <= 8:
        return "Summer %d" % year
    else:
        return "Fall %d" % year

def get_results():
    keywords, options = splunk.Intersplunk.getKeywordsAndOptions()
    cutoff = int(options.get('cutoff', 0))

    results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()

    data = []
    for r in results:
        ts = r["_time"]
        d = datetime.date.fromtimestamp(int(ts))
        r["semester"] = get_semester(d)

    return results

try: 
    results = get_results()
except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))
splunk.Intersplunk.outputResults( results )
