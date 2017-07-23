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


def prepare_company_paste(company, print_file):    
    export = open(print_file, "a")    
    file_line = ""
    print company
    file_line += company["name"]
    for key in company:
        if key == "name":
            continue            
        file_line += ", {0}".format(company[key])
    file_line += "\n"
    export.write(file_line)
    export.close()

def serialize_company(company, print_file):
    export = open(print_file, "a")    
    file_line = ""    
    export.write(json.dumps(company) + "\n")
    export.close()    



dir_name = "company_triage"
export_file = "copy_here.txt"
serialize_file = "serialize_companies.txt"
files = glob.glob(dir_name+"/*")
companies_list = []

for file_set in files[  :-1]:
    companies_buff = open(file_set, 'r')
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



for i, company in enumerate(companies_list):
    call(["sh", "acquire_company_profile.sh", company["profile"]])    
    profile_buff = open("profile_buff.txt", "r")
    profile_string = profile_buff.read()
    tree = html.fromstring(profile_string)
    print "companies left:", len(companies_list) - i    
    test_len = len(tree.xpath("//*"))
    if test_len < 42:
        print "captcha block"
    else:
        if tree.xpath("/html/head/meta[@content='FOUNDER']"):
           companies_list[i]["founder"] = tree.xpath("/html/head/meta[position()=22]/@content").pop()
        else:
            companies_list[i]["founder"] = "founder not found"
    profile_buff.close()
    try:
        prepare_company_paste(company, export_file)
        serialize_company(company, serialize_file)
    except UnicodeEncodeError as e:
        print "error:", e
    time.sleep(20)





