#!/usr/bin/env python
import sys
import requests
import pprint
import glob
import time
import json
from lxml import html, etree
from subprocess import call, check_output
pp = pprint.PrettyPrinter(indent=4)


dir_name = "pages"
files = glob.glob(dir_name+"/*")
companies_list = []

for file_set in files:
    companies_buff = open(files[0], 'r')
    companies_json = json.loads(companies_buff.read())
    companies_html = companies_json["html"]

    tree = html.fromstring(companies_html)
    rows = tree.xpath("//*[@data-_tn]")[1:]

    for i, node in enumerate(rows[1:]):
        company = {}
        company_tree = etree.ElementTree(node)
        company["name"] = company_tree.xpath("//div[@class='company column']//div[@class='name']/a[@class='startup-link']").pop().text
        company["profile"] = company_tree.xpath("//div[@class='company column']//div[@class='name']/a[@class='startup-link']/@href").pop()
        company["website"] = company_tree.xpath("//div[@class='website']/a/@href").pop()
        companies_list.append(company)

    companies_buff.close()






