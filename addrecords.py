"""add_records - Add information to results about when a new record was reached

Usage:

  foo | addrecords client_count | search record=*

"""

import sys,splunk.Intersplunk
import re

try:
    keywords, options = splunk.Intersplunk.getKeywordsAndOptions()
    field = "_raw"
    if keywords:
        field = keywords[0]
    results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()
    results.sort(key=lambda x: x['_time'])

    max = 0
    last_record_time = None
    since_record = 0
    consecutive_records = 0
    for r in results:
        if field not in r:
            continue
        try :
            value = float(r[field])
        except ValueError:
            continue

        if value > max:
            r['record'] = True
            r['since_record'] = since_record
            r['increase'] = value - max
            r['last_record'] = last_record_time
            r['consecutive_records'] = consecutive_records
            max = value
            last_record_time = r['_time']
            since_record = 1
            consecutive_records += 1
        else :
            since_record += 1
            consecutive_records = 0
    results.sort(key=lambda x: x['_time'], reverse=True)
except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

splunk.Intersplunk.outputResults( results )
