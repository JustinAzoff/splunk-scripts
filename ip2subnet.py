"""ip2subnet - truncate ip addresses to the /24 they are on"""

import sys,splunk.Intersplunk
import re


ipregex = r"(?P<ip>((25[0-5]|2[0-4]\d|[01]\d\d|\d?\d)\.){3}(25[0-5]|2[0-4]\d|[01]\d\d|\d?\d))"

def get_ips(line):
    #returns tuples like (1.2.3.4, 3., 3, 4) due to the groups
    return [x[0] for x in re.findall(ipregex, line)]

def get_subnet(line):
    ips = get_ips(line)
    if not ips:
        return
    ip = ips[0]
    parts = ip.split('.')
    return '.'.join(parts[0:3])

try:
    keywords, options = splunk.Intersplunk.getKeywordsAndOptions()
    field = "_raw"
    if keywords:
        field = keywords[0]
    results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()
    for r in results:
        if field not in r:
            continue
        r['subnet'] = get_subnet(r[field])
except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

splunk.Intersplunk.outputResults( results )
