#!/usr/bin/env python
import sys
import requests
import pprint
import glob
import time
import unicodedata
import json
from lxml import html, etree
from subprocess import call, check_output
pp = pprint.PrettyPrinter(indent=4)


def prepare_company_paste(contact_site, print_file):    
    export = open(print_file, "a")
    file_line = contact_site    
    file_line += "\n"
    export.write(file_line)
    export.close()

def import_list_company_sites(import_fileName):
    import_file = open(import_fileName, "r")
    tmp_str = import_file.read()
    import_file.close()
    return (tmp_str.split("\n"))

def determine_tld_domain(url):
    tld_list = ['.com', '.net', '.tech', '.co', '.io', '.tv', '.org', '.network', '.ca', '.life', '.ly', '.me.uk', '.me', '.us', '.sc', '.ai', '.mobi', '.ru', '.is', '.fi', '.eu', '.ie', '.video', '.cm', '.gg', '.ng', '.audio', '.global', '.in', '.bio', '.work', '.am', '.education', '.systems', '.aero', '.earth', '.travel']
    dirty_domain = ""
    tld = ""

    for item in tld_list:
        if item in url:            
            dirty_domain = url.split(item)[0]
            tld = item
            break          

    if tld == "":
        print "no tld found for url: {0}".format(url)  
        return None      

    dirty_domain = dirty_domain.split("//")[1]
    domain = dirty_domain.split(".")[-1]
    return (tld, domain)

def prepare_website(url):
    site = {}

    if "not" in url[:5]:
        return None

    site['raw'] = url    
    tld_domain = determine_tld_domain(url)

    if tld_domain == None:
        return None

    site['tld'] = tld_domain[0]
    site['domain'] = tld_domain[1]
    site['host'] = site['domain'] + site['tld']
    return (site)

def prepare_headers(website):
    headers = {'Host': website['host']}
    headers['Connection'] = 'keep-alive'
    headers['Cache-Control'] = 'max-age=0'
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*'
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['Accept-Language'] = 'en-US,en;q=0.5'
    return (headers)

def fetch_contact_patterns(contact_file):
    contact_file = open(contact_file, 'r')    
    contact_json = json.loads(contact_file.read())
    contact_file.close()

    del contact_json['bottom of page']
    del contact_json['none']
    del contact_json['about#contact-us']
    del contact_json['about/#contact']

    keys = list(contact_json.keys())
    tuples = [(key, contact_json[key]) for key in keys]
    tuples.sort(key=lambda x: x[1], reverse=True)
    contact_patterns = [tup[0] for tup in tuples]
     
    return contact_patterns

def attempt_contact(website, format):
    domain = "{domain}"
    tld = "{tld}"
    contact_url = website['raw'] + '/' + format
    reformat = False

    if domain in format:
        format = format.replace(domain, website['domain'])
        reformat = True

    if tld in format:
        format = format.replace(tld, website['tld'][1:])
        reformat = True

    if reformat == True:
        contact_url = "https://" + format

    r = requests.get(contact_url)
    
    if "Help Center Closed | Zendesk" in r.text:
        r.status_code = 404
    
    return (r.status_code, contact_url)
    
def add_to_stats(stats_set, stats, pattern):
    if (pattern in stats_set):
        stats[pattern] += 1
    else:
        stats_set.add(pattern)
        stats[pattern] = 1
    stats['total'] += 1

import_file = "input.find_contact_page"
contact_file = "../contact_page"
export_file = "data.find_contact_page"
stat_file = "stats.find_contact_page"

site_list = import_list_company_sites(import_file)
site_list = site_list[53 + 370 + 945 + 292:]
stats = {'total': 0}
stats_set = set()

for i, site in enumerate(site_list):
    
    print "i:", i, "site:", site
    website = prepare_website(site)
    
    if website == None:
        print "no url"    
        prepare_company_paste("invalid url for: " + site, export_file)
        continue

    pattern_list = fetch_contact_patterns(contact_file)

    success = False
    changed = False
    for pattern in pattern_list:        
        try:
            contact_attempt = attempt_contact(website, pattern)
            if (contact_attempt[0] == 200):
                prepare_company_paste(contact_attempt[1], export_file)
                success = True
                print "     200:", contact_attempt[1]
                break    
            print "     404:", pattern
        except requests.exceptions.ConnectionError, e:            
            if changed == False:
                website['raw'] = "http://" + website['raw'].split("https://")[1]
                changed = True
                try:
                    contact_attempt = attempt_contact(website, pattern)
                    if (contact_attempt[0] == 200):
                        prepare_company_paste(contact_attempt[1], export_file)
                        success = True
                        print "     200:", contact_attempt[1]
                        break    
                    print "     404:", pattern
                except requests.exceptions.ConnectionError, e:
                    print "     connection error:", pattern
                except requests.exceptions.TooManyRedirects, e:
                    print "     connection error:", pattern
            else:
                print "     connection error:", pattern
        except requests.exceptions.TooManyRedirects, e:
            if changed == False:
                website['raw'] = "http://" + website['raw'].split("https://")[1]
                changed = True
                try:
                    contact_attempt = attempt_contact(website, pattern)
                    if (contact_attempt[0] == 200):
                        prepare_company_paste(contact_attempt[1], export_file)
                        success = True
                        print "     200:", contact_attempt[1]
                        break    
                    print "     404:", pattern
                except requests.exceptions.ConnectionError, e:
                    print "     connection error:", pattern
                except requests.exceptions.TooManyRedirects, e:
                    print "     connection error:", pattern
            else:
                print "     connection error:", pattern

    if success == False:
        prepare_company_paste("check bottom of page?", export_file)
        pattern = "no match"
        print "     set: bottom of page"

    add_to_stats(stats_set, stats, pattern)
    if i % 10 == 0:
        stats_file = open(stat_file, "a")
        stats_file.write(json.dumps(stats) + '\n')
        stats_file.close


