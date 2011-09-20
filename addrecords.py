"""add_records - Add information to results about when a new record was reached"""

import sys,splunk.Intersplunk
import re

try:
    keywords, options = splunk.Intersplunk.getKeywordsAndOptions()
    field = "_raw"
    if keywords:
        field = keywords[0]
    results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()
    results.sort(key=lambda x: x['_time'],reverse=True)

    max = 0
    since_record = 0
    for r in results:
        if field not in r:
            continue
        value = r[field]
        if value > max:
            r['record'] = True
            r['since_record'] = since_record
            r['increase'] = value - max
            max = value
            since_record = 0
        else :
            since_record += 1
except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

splunk.Intersplunk.outputResults( results )
