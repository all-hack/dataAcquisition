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


def prepare_company_paste(company, print_file):    
    export = open(print_file, "a")    
    file_line = ""    
    file_line += company["website"]
    for key in company:
        if key == "website":
            continue            
        file_line += ", {0}".format(company[key])
    file_line += "\n"
    export.write(file_line)
    export.close()

url = "http://matter.vc/community/"
headers = {'Host': 'matter.vc'}
headers['Connection'] = 'keep-alive'
headers['Cache-Control'] = 'max-age=0'
headers['Upgrade-Insecure-Requests'] = '1'
headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
headers['Accept-Encoding'] = 'gzip, deflate'
headers['Accept-Language'] = 'en-US,en;q=0.8'
headers['Cookie'] = 'X-Mapping-fjhppofk=F5BDEDF797F14BB7734F4BA3EDCBBC9E; _cb_ls=1; _ga=GA1.2.125445617.1502407660; _gid=GA1.2.1423102991.1502407660; _gat=1; _cb=CWFenmgnzOkkpMAY; _chartbeat2=.1502407666901.1502415430295.1.nGnBcYqUXMCcFUUMBT_ctCRdpl; _cb_svref=null; _chartbeat4=t=KQT7XCWcgNTw57LxDMX0r8Dau5D5&E=1&EE=1&x=429&c=0.08&y=7288&w=431'

r = requests.get(url, headers=headers)

export_file = "data.matter_vc"
companies_list = []
companies_set = set()

tree = html.fromstring(r.text)
rows = tree.xpath("//a[@class='grid-image avia-hover-fx']")

# print(etree.tostring(rows[1], pretty_print=True))

for i, node in enumerate(rows):
    company = {}
    profile = ""
    
    node = etree.ElementTree(node)    
    profile = node.xpath("@href").pop()
    print "companies hit so far:", i + 1, "next:", profile
    r = requests.get(profile, headers=headers)        
    profile_tree = html.fromstring(r.text)
    try: 
        company["name"] = profile_tree.xpath("/html/head/title").pop(0).text.split("|")[1].strip()
    except IndexError, e:
        company['name'] = profile

    try: 
        company["website"] = profile_tree.xpath("//li/h4/a/@href").pop(0)
    except IndexError, e:
        company["website"] = "not on {0}".format(url)
    
    try: 
        company["email"] = profile_tree.xpath("//li[4]/h4/a/@href").pop(0).split("mailto:")[1]
    except IndexError, e:
        company["email"] = "not on {0}".format(url)
        
    if company['name'] not in companies_set:
        companies_list.append(company)
        companies_set.add(company['name'])

    try:
        prepare_company_paste(company, export_file)
    except UnicodeEncodeError as e:
        print "error:", e

    time.sleep(7)

print "len(companies):", len(companies_list)






