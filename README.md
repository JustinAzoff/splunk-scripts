Splunk scripts
==============

ip2subnet.py
------------

ip to subnet - truncate ip addresses to the /24 they are on


make_oui_table.py
-----------------

make oui table - download the oui table from the ieee and build a table of oui
prefix, owner
also, normalize spelling of common owners that have multiple spellings

makeyearly.py
-------------

make yearly - collapse yearly data on top of itself for reporting multiple
years on a single overlayed chart

ua2os.py
--------

ua to os - from a user agent return operating system, architecture, and browser
