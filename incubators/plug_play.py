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
    # print company
    file_line += company["website"]
    for key in company:
        if key == "website":
            continue            
        file_line += ", {0}".format(company[key])
    file_line += "\n"
    export.write(file_line)
    export.close()

url = "http://plugandplaytechcenter.com/startup-database/"

r = requests.get(url)

export_file = "data.plug_play"
companies_list = []
companies_set = set()
tree = html.fromstring(r.text)
rows = tree.xpath("//li[@class='pnp-image-text-no-link col-xs-6 col-sm-4 col-md-3']")

# print rows
# print(etree.tostring(rows[1], pretty_print=True))

for i, node in enumerate(rows):
    company = {}
    company_tree = etree.ElementTree(node)    
    try: 
        company["name"] = company_tree.xpath("//h3").pop(0).text        
    except IndexError, e:
        print(etree.tostring(node, pretty_print=True))

    try: 
        company["website"] = company_tree.xpath("//a/@href").pop(0)
    except IndexError, e:
        company["website"] = "not on {0}".format(url)
    if company['name'] not in companies_set:
        companies_list.append(company)
        companies_set.add(company['name'])





for i, company in enumerate(companies_list):    
    print "companies left:", len(companies_list) - i
    try:
        prepare_company_paste(company, export_file)
    except UnicodeEncodeError as e:
        print "error:", e

print "len(companies):", len(companies_list)



