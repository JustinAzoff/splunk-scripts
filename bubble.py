"""bubble - re-emit a log record with all superdomains

    | bubble [field=host]

add 'superhost' and 'parts' fields. 

"""

import sys,splunk.Intersplunk
import re

ipregex = r"(?P<ip>((25[0-5]|2[0-4]\d|[01]\d\d|\d?\d)\.){3}(25[0-5]|2[0-4]\d|[01]\d\d|\d?\d))"

ip_rex = re.compile(ipregex)

def super_domains(host):
    """
    FIXME
    >>> list(super_domains("a.b.com"))
    {'host': '*.b.com', 'parts': 2}, {'host': '*.com', 'parts': 1}]
    >>> list(super_domains("1.2.3.4"))
    [{'host': '1.2.3.*', 'parts': 3}, {'host': '1.2.*', 'parts': 2}, {'host': '1.*', 'parts': 1}]
    """

    parts = host.split(".")
    num_parts = len(parts)
    yield dict(superhost=host, parts=num_parts)
    if ip_rex.match(host):
        for x in range(1,4):
            host = '.'.join(parts[:-x]) + '.*'
            p = num_parts - x
            yield dict(superhost=host, parts=p)
    else:
        for x in range(num_parts-1,0,-1):
            host = '*.' + '.'.join(parts[-x:])
            p = x
            yield dict(superhost=host, parts=p)

try:
    keywords, options = splunk.Intersplunk.getKeywordsAndOptions()
    field = options.get('field', 'hostname')

    results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()
    newresults = []
    for r in results:
        if field not in r:
            continue
        for info in super_domains(r[field]):
            info.update(r)
            newresults.append(info)
except:
    import traceback
    stack =  traceback.format_exc()
    newresults = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

splunk.Intersplunk.outputResults( newresults )
