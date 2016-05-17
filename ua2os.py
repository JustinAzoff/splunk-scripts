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
    ('Windows NT 6.3',      'Windows 8.1'),
    ('Windows NT 10.0',     'Windows 10'),
    ('OS X 10.(\d)',        'Mac OS X 10.%s.x'),
    ('SunOS',               'Solaris'),
    ('droid',               'Android'),
    ('Windows',             'Windows - Other'),
    ('iPad[^d]',            'iPad'),
    ('iPod',                'iPod'),
    ('iPhone',              'iPhone'),
    ('OS X',                'Mac OS X - Other'),
    ('Darwin',              'Mac OS X - Other'),
    ('Linux ',              'Linux'),
    ('winhttp',             'Windows - Other'),
    ('MSIE 4.0;',           'Windows - Other'),
    ('Microsoft',           'Windows - Other'),
    ('Win32',               'Windows - Other'),
    ('BlackBerry',          'BlackBerry'),
    ('BB10',                'BlackBerry 10'),
    ('RIM (\S+ \S+ \S+)',   'BlackBerry %s'),
    ('OS/2',                'OS/2'),
    ('urlgrabber/.* yum',   'Linux - RedHat/Fedora'),
    ('Skype for Macintosh', 'Mac OS X - Other'),
    ('Xbox Live Client',    'Xbox'),
    ('hpwOS/(\S+)',         'HP webOS %s'),
    ('J2ME',                'JVM Micro Edition'),
    ('CrOS',                'Chromium OS'),
    ('FreeBSD',             'FreeBSD'),
)

browser_mapping = (
    ('MSIE 7.*Trident/4.0', 'Internet Explorer 8.0'),
    ('MSIE ([9876]).0',     'Internet Explorer %s.0'),
    ('MSIE 10.0',           'Internet Explorer 10.0'),
    ('Trident/7.0; rv:11.0','Internet Explorer 11.0'),
    ('droid',               'Android'),
    ('Chrome',              'Chrome'),
    ('Mobile.*Safari',      'Safari - mobile'),
    ('i(pod|pad|phone).*(Safari|AppleWebKit)', 'Safari - mobile'),
    ('Safari/',             'Safari'),
    ('iTunes',              'iTunes'),
    ('Firefox/(\d+)',       'Firefox %s'),
    ('MSIE 5.00',           'Internet Explorer 5.0'),
    ('MSIE',                'Internet Explorer - Other'),
    ('AppleWebKit',         'Safari'),
    ('Google Update',       'Google Update'),
    ('Opera Mini',          'Opera Mini'),
    ('Opera',               'Opera'),
    ('urlgrabber/.* yum',   'yum'),
    ('BlackBerry',          'Blackberry'),
    ('Googlebot',           'Googlebot'),
    ('Baiduspider',         'Baidubot'),
    ('NING/\d',             'Ning'),
    ('msnbot/\d',           'msnbot'),
    ('gsa-crawler',         'Google Search Appliance'),
    ('Ezooms/\d',           'Ezooms'),
    ('bingbot',             'bingbot'),
    ('YandexBot',           'yandexbot'),
    ('Genieo',              'genieo'),
    ('Apple-PubSub',        'Apple PubSub'),
    ('Java/\d',             'Java'),
    ('Warp (\S+)',          'Warp %s'),
    ('wOSBrowser/(\S+)',    'webOS Browser %s'),
    ('SeaMonkey/(\S+)',     'SeaMonkey %s'),
)

arch_mapping = (
    ('Windows .. 5.2',                          'x64'),
    ('x64',                     		'x64'),
    ('Win64',                                   'x64'),
    ('Windows .. 6.1.*WOW64',                   'x64'),
    ('Windows .. 6.([012])\; Trident/',         'i386'),
    ('i386',               	 		'i386'),
    ('i686',                                    'i686'),
    ('x86_64',              			'x64'),
    ('amd64',                                   'x64'),
    ('PPC',                 			'PowerPC'),
    ('Power.{1,3}Macint',   			'PowerPC'),
    ('droid',               			'Android'),
    ('iPad[^d]',            			'iPad'),
    ('iPod',                			'iPod'),
    ('iPhone',              			'iPhone'),
    ('Intel',               			'Intel'),
    ('BlackBerry (\d+)',          		'BlackBerry %s'),
    ('BlackBerry',				'BlackBerry'),
    ('BB10',                                    'BlackBerry 10'),
    ('Playbook',                                'BlackBerry Playbook'),
    ('hp-tablet',                               'HP Tablet'),
    ('armv(\d+)',                               'ARM v%s'),
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
