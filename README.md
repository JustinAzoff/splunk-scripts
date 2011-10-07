Splunk scripts
==============

ip2subnet.py
------------

ip to subnet - truncate ip addresses to the /24 they are on.


make_oui_table.py
-----------------

make oui table - download the oui table from the ieee and build a table of oui
prefix, owner.  Also, normalize spelling of common owners that have multiple
spellings.

makeyearly.py
-------------

make yearly - collapse yearly data on top of itself for reporting multiple
years on a single overlayed chart.

ua2os.py
--------

ua to os - from a user agent return operating system, architecture, and browser.

addsemester.py
--------------
Add a semester field so you can report by semester.

addrecords.py
-------------
Add information about record values

 * record - Was this a record number for this value
 * since_record - How many values have been since since the last record
 * last_record - The time of the last record
 * consecutive_records - The number of records in a row
 * increase - The difference between the last record and the new record
