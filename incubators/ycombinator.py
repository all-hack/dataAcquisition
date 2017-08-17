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


def prepare_company_paste(line, print_file):    
    export = open(print_file, "a")    
    file_line = ""    
    file_line += line
    file_line += "\n"
    export.write(file_line)
    export.close()

website_export_file = "data.ycombinator_websites"
name_export_file = "data.ycombinator_names"
companies_list = []
companies_set = set()

yc_result_file = open("yc_results", 'r')
yc_result_text = yc_result_file.read()
rows = yc_result_text.split("\n")
delim1 = "VM1551:2 "
delim2 = " || "

for i, node in enumerate(rows):
    company = {}

    print "companies hit so far:", i + 1
    node = node.split(delim1)[1]
    company["name"] = node.split(delim2)[1]
    company["website"] = node.split(delim2)[0]    
        
    if company['name'] not in companies_set:
        companies_list.append(company)
        companies_set.add(company['name'])

    try:
        prepare_company_paste(company['website'], website_export_file)
        prepare_company_paste(company['name'], name_export_file)
    except UnicodeEncodeError as e:
        print "error:", e



print "len(companies):", len(companies_list)






