#!/usr/bin/env python
import sys
import requests
import pprint
import glob
import time
import unicodedata
import json
import os
import email
import smtplib
import imaplib
from lxml import html, etree
from subprocess import call, check_output
pp = pprint.PrettyPrinter(indent=4)

def save_master_json(master_json, data_fileName):
    data_file = open(data_fileName, "w")
    json.dump(master_json, data_file)
    data_file.close()

def save_master_list(list_item, data_fileName):
    data_file = open(data_fileName, "a")
    data_file.write(list_item)
    data_file.close()

def import_master_jason(data_fileName):
    master_json = json.load(open(data_fileName, "r"))
    master_set = set()
    for key in master_json.keys():
        master_set.add(key)
    return (master_json, master_set)
    

def import_list_company_sites(import_fileName):
    import_file = open(import_fileName, "r")
    tmp_str = import_file.read()
    import_file.close()
    return (tmp_str.split("\n"))

def determine_tld_domain(url, tld_list):
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

def prepare_website(url, tld_file):
    site = {}

    if "not" in url[:5]:
        return None

    site['raw'] = url    
    tld_domain = determine_tld_domain(url, tld_file)

    if tld_domain == None:
        return None

    site['tld'] = tld_domain[0]
    site['domain'] = tld_domain[1]
    site['host'] = site['domain'] + site['tld']
    return site

def prepare_email_json(website, generic_email_json):
    domain = "{domain}"
    tld = "{tld}"
    for key in generic_email_json.keys():
        format = key
        format = format.replace(domain, website['domain'])
        format = format.replace(tld, website['tld'])
        generic_email_json[format] = generic_email_json.pop(key)
    return generic_email_json

def prepare_company_paste(contact_site, print_file):    
    export = open(print_file, "a")
    file_line = contact_site    
    file_line += "\n"
    export.write(file_line)
    export.close()

def fetch_email_patterns(email_file):
    email_file = open(email_file, 'r')
    email_json = json.loads(email_file.read())
    email_file.close()
    return email_json

def fetch_tld_list(tld_file):
    tld_file = open(tld_file, "r")
    tld_list = tld_file.readline().split(", ")    
    return tld_list
    
def add_to_stats(stats_set, stats, pattern):
    if (pattern in stats_set):
        stats[pattern] += 1
    else:
        stats_set.add(pattern)
        stats[pattern] = 1
    stats['total'] += 1

def send_email_yandex(website, email_json):
    FROM_EMAIL  = os.environ['MAIL_TEST_TRIAL_U'] 
    FROM_PWD    = os.environ['MAIL_TEST_TRIAL_P']
    SMTP_SERVER = "smtp.yandex.com"
    SMTP_PORT   = 587
    SMTP_SET = "{0}:{1}".format(SMTP_SERVER, SMTP_PORT)
    
    server = smtplib.SMTP(SMTP_SET)    
    server.ehlo()
    server.starttls()
    server.login(FROM_EMAIL,FROM_PWD)
    subj = "holiday property"
    msg = "Hello\n\nwww.Self-catering-breaks.com is now becoming one of the largest sites on the internet\n\nfor people who wish to list their own properties\n\nWe already have 1000's of properties listed but want to make sure you already have\n\nlisted your properties.\n\nSo please feel free to add your property or properties.\n\nFirstly register and you will be emailed an authorisation key.\n\nThanks for your time and please pass this email onto anyone you think may be\n\ninterested to list for free."

    print "sending emails to {0}".format(website['raw'])
    for user in email_json.keys():
        MESSAGE_FORMAT = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" %(FROM_EMAIL, user, subj, msg)
        server.sendmail(FROM_EMAIL, user, MESSAGE_FORMAT)        
        email_json[user] = 1

    server.quit()
    return email_json

def guess_emails():
    for i, site in enumerate(site_list):
        print "i:", i, "site:", site

        website = prepare_website(site, tld_list)    
        if website == None:
            print "no url"
            save_master_list("no url for: " + site + "\n", list_file)
            continue
        if website['host'] in master_set:
            save_master_list(website['host'] + "\n", list_file)
            continue

        email_json = prepare_email_json(website, generic_email_json)
        email_json = send_email_yandex(website, email_json)
        master_json[website["host"]] = email_json
        save_master_list(website['host'] + "\n", list_file)
        save_master_json(master_json, data_file)

def read_email_yandex(email_json):
    FROM_EMAIL  = os.environ['MAIL_TEST_TRIAL_U'] 
    FROM_PWD    = os.environ['MAIL_TEST_TRIAL_P']
    IMAP_SERVER = "imap.yandex.com"    
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()    
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    print first_email_id
    print latest_email_id

    for i in range(latest_email_id, first_email_id, -1):
        typ, data = mail.fetch(i, '(RFC822)' )            
        if i == 5:
            for response_part in data:
                # print "response_part"
                # print response_part
                # print "0"
                # print response_part[0]
                # print "\n\n"
                # print "1"
                # print response_part[1]
                # print "\n\n"
                # print "\n\n\n\n"
                # if "inquiries@dropbox.com" in response_part[1]:
                #     print "wooo"
                
                # print email_json
                # for key in email_json.keys():
                #     if key in response_part:
                #         print "wow this worked"
                # print response_part[2]
                if isinstance(response_part, tuple):
                #     print ""
                    msg = email.message_from_string(response_part[1])                    
                    # for payload in msg.get_payload(0, decode=True):
                    #     pp.pprint(payload)
                    # print msg.get_payload(0)
                    print msg.get_payload(1)


                #     # if 'postmaster' in msg["from"]:
                #         # continue
                #     print msg.keys()
                #     # print ''                
                #     for key in msg.keys():
                #         print "{0}: {1}\n".format(key, msg[key])

                #     email_subject = msg['subject']
                #     email_from = msg['from']
                #     # if msg['X-Failed-Recipients'] == None:
                #         # continue
                #     # index_user = user_list.index(msg['X-Failed-Recipients'])
                #     # print ("from: {0}".format(email_from))
                #     # print ("to: {0}".format(msg['to']))
                #     # print ("subject: {0}".format(email_subject))
                #     # print ("X-Failed-Recipients: {0}".format(msg['X-Failed-Recipients']))
                #     # print "index in user_list: {0}".format(index_user)
                #     # print "user_list[{0}]: {1}".format(index_user, user_list[index_user])
                #     # user_list[index_user] = "searching for email"
                #     # print "i: {0}, user_list[{1}] = {2}".format(i, index_user, user_list[index_user])
    # return user_list



import_file = "input.guess_email"
email_file = "../generic_emails"
export_file = "paste.guess_email"
data_file = "data.guess_email"
list_file = "data.list.guess_email"
stat_file = "stats.guess_email"
tld_file = "../tld_list"

tld_list = fetch_tld_list(tld_file)
generic_email_json = fetch_email_patterns(email_file)

site_list = import_list_company_sites(import_file)
site_list = site_list[:3]

stats = {'total': 0}
stats_set = set()

master_json = {}
master_set = set()

data_file_exist = glob.glob(data_file)

if data_file_exist:
    dict_set = import_master_jason(data_file)
    master_json = dict_set[0]
    master_set = dict_set[1]

# guess_emails()

email_json = master_json['dropbox.com']

read_email_yandex(email_json)




