"""bubble - re-emit a log record with superdomain

    | bubble [field=host] [parts=3]

adds 'superhost' field

"""

import sys,splunk.Intersplunk
import re

ipregex = r"(?P<ip>((25[0-5]|2[0-4]\d|[01]\d\d|\d?\d)\.){3}(25[0-5]|2[0-4]\d|[01]\d\d|\d?\d))"

ip_rex = re.compile(ipregex)

def super_domain(host, output_parts):
    parts = host.split(".")
    num_parts = len(parts)
    if output_parts > num_parts:
        return host

    if ip_rex.match(host):
        host = '.'.join(parts[:-output_parts])
    else:
        host = '.'.join(parts[-output_parts:])

    return host

def add_superhost(results, field, num_parts):
    for r in results:
        if field not in r:
            continue
        d = super_domain(r[field], num_parts)
        r['superhost'] = d
        yield r
    

try:
    keywords, options = splunk.Intersplunk.getKeywordsAndOptions()
    field = options.get('field', 'hostname')
    num_parts = int(options.get('parts', 2))

    results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()
    results = list(add_superhost(results, field, num_parts))
            
except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

splunk.Intersplunk.outputResults( results )
