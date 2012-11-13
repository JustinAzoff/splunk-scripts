"""ua to os - from a user agent return operating system, architecture, and browser"""

import sys,splunk.Intersplunk
import re

os_mapping = (
    ('Windows .. 5.1',      'Windows XP'),
    ('Windows .. 5.2',      'Windows XP'),
    ('Windows NT 6.0',      'Windows Vista'),
    ('Windows 6.0',         'Windows Server 2008'),
    ('Windows NT 6.1',      'Windows 7'),
    ('Windows NT 6.2',      'Windows 8'),
    ('OS X 10.(\d)',        'MAC OS X 10.%s.x'),
    ('SunOS',               'Solaris'),
    ('droid',               'Android'),
    ('Windows',             'Windows - Other'),
    ('iPad',                'ipad'),
    ('iPod',                'ipod'),
    ('iPhone',              'iphone'),
    ('OS X',                'MAC OS X other'),
    ('Darwin',              'MAC OS X other'),
    ('Linux ',              'Linux'),
    ('winhttp',             'Windows - Other'),
    ('MSIE 4.0;',           'Windows - Other'),
    ('Microsoft',           'Windows - Other'),
    ('Win32',               'Windows - Other'),
    ('BlackBerry',          'BlackBerry'),
    ('urlgrabber/.* yum',   'Linux - redhat/fedora'),
    ('Skype for Macintosh', 'MAC OS X other'),
    ('Xbox Live Client',    'Xbox'),
)

browser_mapping = (
    ('MSIE 7.*Trident/4.0', 'Internet Explorer 8.0'),
    ('MSIE ([0-9]{1,2}).0', 'Internet Explorer %s.0'),
    ('droid',               'Android'),
    ('Chrome',              'Chrome'),
    ('Mobile.*Safari',      'Safari - mobile'),
    ('i(pod|pad|phone).*(Safari|AppleWebKit)', 'Safari - mobile'),
    ('Safari/',             'Safari'),
    ('iTunes',              'iTunes'),
    ('Firefox/(\d)',        'Firefox %s'),
    ('MSIE 5.00',           'Internet Explorer 5.0'),
    ('MSIE',                'Internet Explorer - Other'),
    ('AppleWebKit',         'Safari'),
    ('Google Update',       'Google Update'),
    ('Opera',               'Opera'),
    ('urlgrabber/.* yum',   'yum'),
    ('BlackBerry',          'Blackberry'),
)

arch_mapping = (
    ('Windows .. 5.2',      'x64'),
    ('x64',                 'x64'),
    ('i386',                'i386'),
    ('x86_64',              'x64'),
    ('PPC',                 'PowerPC'),
    ('Power.{1,3}Macint',   'PowerPC'),
    ('droid',               'android'),
    ('iPad',                'ipad'),
    ('iPod',                'ipod'),
    ('iPhone',              'iphone'),
    ('Intel',               'Intel'),
    ('BlackBerry',          'BlackBerry'),
    ('ARM',                 'ARM'),
)

os_mapping      = [(re.compile(a, re.IGNORECASE),b) for (a,b) in os_mapping]
browser_mapping = [(re.compile(a, re.IGNORECASE),b) for (a,b) in browser_mapping]
arch_mapping    = [(re.compile(a, re.IGNORECASE),b) for (a,b) in arch_mapping]

def get_thing(line, mapping):
    for r, name in mapping:
        match = r.search(line)
        if match:
            if '%' in name:
                return name % match.groups()
            else:
                return name
    return 'unknown'

def get_ua_info(line):
    i = {}
    i['operating_system'] = get_thing(line, os_mapping)
    i['architecture']     = get_thing(line, arch_mapping)
    i['browser']          = get_thing(line, browser_mapping)
    return i

try:
    results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()
    for r in results:
        if "_raw" not in r:
            continue
        info = get_ua_info(r['_raw'])
        r.update(info)
except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

splunk.Intersplunk.outputResults( results )
