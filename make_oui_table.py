#!/usr/bin/env python 
import os
import httplib2
import csv
import re

URL="http://standards.ieee.org/regauth/oui/oui.txt"


common_mappings = (
    ('^apple[, ]', 'Apple'),
    ('^Hon Hai Precision', 'Hon Hai Precision Ind.'),
    ('^Intel', 'Intel'),
    ('^Gemtek Technology', 'Gemtek Technology'),
    ('^askey ', 'Askey computer corp'),
    ('^LITE-ON Technology Corp', 'Liteon Technology Corporation'),
    ('^Liteon Tech Corp', 'Liteon Technology Corporation'),
    ('^RIM', 'Research In Motion'),
    ('^RIM Testing Services', 'Research In Motion'),
    ('^AzureWave Technologies', 'AzureWave Technologies'),
    ('^High Tech Computer Corp', 'HTC Corporation'),

)

def get_file():
    http = httplib2.Http(os.path.expanduser("~/.httplib2_cache"))
    resp, content = http.request(URL)
    return content

def get_hex_records(data):
    for line in data:
        if 'hex' in line:
            yield line

def parse_records(hex):
    for x in hex:
        parts = x.split("\t")
        mac = parts[0][:8].replace("-",":").lower()
        owner  = fix_owner(parts[2])
        yield mac, owner

def fix_owner(owner):
    for regex, new_name in common_mappings:
        if re.search(regex, owner, re.IGNORECASE):
            return new_name
    return owner

def main():
    data = get_file().splitlines()
    hex = get_hex_records(data)
    records = parse_records(hex)

    f = csv.writer(open("oui_table.csv",'w'))
    f.writerow(("oui","owner"))
    for x in records:
        f.writerow(x)

if __name__ == "__main__":
    main()
