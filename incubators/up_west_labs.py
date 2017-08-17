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


url = "http://upwestlabs.com/portfolio/"

# click more until your out of pages and then download the html
# r = requests.get(url)

tree_file = open("tree.up_west_labs.html", 'r')
tree_string = tree_file.read()

export_file = "data.up_west_labs"
companies_list = []
companies_set = set()

tree = html.fromstring(tree_string)
rows = tree.xpath("//div[@class='f_canvas']/a")
print len(rows)

# print(etree.tostring(rows[1], pretty_print=True))


for i, node in enumerate(rows):
    company = {}
    profile = ""
    print "companies hit so far:", i + 1

    node = etree.ElementTree(node)
    
    try: 
        company["name"] = node.xpath("//h2").pop(0).text.lower()   
    except IndexError, e:
        company['name'] = "not on {0}".format(url)
        
    try: 
        company["website"] = node.xpath("@href").pop(0)        
    except IndexError, e:
        company["website"] = "not on {0}".format(url)
        
    if company['name'] not in companies_set:
        companies_list.append(company)
        companies_set.add(company['name'])

    try:
        prepare_company_paste(company, export_file)
    except UnicodeEncodeError as e:
        print "error:", e


print "len(companies):", len(companies_list)






