#!/usr/bin/env python
import sys
import requests
import pprint
import glob
import time
import json
import os
import smtplib
import time
import imaplib
import email
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

def read_email_from_gmail(user_list):    
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )            
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    if 'postmaster' in msg["from"]:
                        continue
                    # print msg.keys()
                    # print ''
                    # for key in msg.keys():
                    #     print "{0}: {1}".format(key, msg[key])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    if msg['X-Failed-Recipients'] == None:
                        continue
                    index_user = user_list.index(msg['X-Failed-Recipients'])
                    # print ("from: {0}".format(email_from))
                    # print ("to: {0}".format(msg['to']))
                    # print ("subject: {0}".format(email_subject))
                    # print ("X-Failed-Recipients: {0}".format(msg['X-Failed-Recipients']))
                    # print "index in user_list: {0}".format(index_user)
                    # print "user_list[{0}]: {1}".format(index_user, user_list[index_user])
                    user_list[index_user] = "searching for email"
                    print "i: {0}, user_list[{1}] = {2}".format(i, index_user, user_list[index_user])
        return user_list
    except Exception, e:
        print str(e)

def send_email_yandex:
    FROM_EMAIL  = os.environ['MAIL_TEST_TRIAL_U'] 
    FROM_PWD    = os.environ['MAIL_TEST_TRIAL_P']
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT   = 465
    # print "sending email[{0}]: {1}".format(i, user_list[-1])
    # Subj = "holiday property"
    # msg = "Hello\n\nwww.Self-catering-breaks.com is now becoming one of the largest sites on the internet\n\nfor people who wish to list their own properties\n\nWe already have 1000's of properties listed but want to make sure you already have\n\nlisted your properties.\n\nSo please feel free to add your property or properties.\n\nFirstly register and you will be emailed an authorisation key.\n\nThanks for your time and please pass this email onto anyone you think may be\n\ninterested to list for free."
    # MESSAGE_FORMAT = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" %(FROM_EMAIL, user_list[-1],Subj,msg)
    # server = smtplib.SMTP('smtp.gmail.com:587')
    # server.starttls()
    # server.login(FROM_EMAIL,FROM_PWD)
    # # print user_list
    # server.sendmail(FROM_EMAIL, user_list[-1], MESSAGE_FORMAT)
    # server.quit()








# copy_emails_file = "tested_emails.txt"
# serialized_file = "serialize_companies.txt"
# FROM_EMAIL  = os.environ['MAIL_TEST_TRIAL_U'] 
# FROM_PWD    = os.environ['MAIL_TEST_TRIAL_P']


# mail = imaplib.IMAP4_SSL(SMTP_SERVER)
# mail.login(FROM_EMAIL,FROM_PWD)
# mail.select('inbox')
# type, data = mail.search(None, 'ALL')
# mail_ids = data[0]
# id_list = mail_ids.split()
# first_email_id = int(id_list[0])
# latest_email_id = int(id_list[-1])

# user_list = []

# import_file = open(serialized_file, "r")
# import_string = import_file.read()
# import_lines = import_string.split("\n")
# company_list = []

# for i, line in enumerate(import_lines[:-1]):
#     # if line == import_lines[0] or line == import_lines[1]:
#     #     continue    

#     company = json.loads(line)
#     company_list.append(company)
    
#     toaddrs = ""

#     domain = "".join(company["website"].split("www."))
#     domain = "".join(domain.split("https"))
#     domain = "".join(domain.split("http"))
#     domain = "".join(domain.split("://"))
#     domain = "".join(domain.split("/"))
#     domain = "".join(domain.split("?utm_source=angellist"))
#     domain = "".join(domain.split("?referer=angellist"))
#     domain = domain.lower()

#     user = company['founder'].split(" ")[0].lower()    
#     user_list.append("{0}@{1}".format(user, domain))        
#     # if i <= 170:
#     #     "sending email[171]: jin@originalstitch.com"
#     #     print "already sent email[{0}]: {1}".format(i, user_list[-1])
#     #     continue

#     # print "sending email[{0}]: {1}".format(i, user_list[-1])
#     # Subj = "holiday property"
#     # msg = "Hello\n\nwww.Self-catering-breaks.com is now becoming one of the largest sites on the internet\n\nfor people who wish to list their own properties\n\nWe already have 1000's of properties listed but want to make sure you already have\n\nlisted your properties.\n\nSo please feel free to add your property or properties.\n\nFirstly register and you will be emailed an authorisation key.\n\nThanks for your time and please pass this email onto anyone you think may be\n\ninterested to list for free."
#     # MESSAGE_FORMAT = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" %(FROM_EMAIL, user_list[-1],Subj,msg)
#     # server = smtplib.SMTP('smtp.gmail.com:587')
#     # server.starttls()
#     # server.login(FROM_EMAIL,FROM_PWD)
#     # # print user_list
#     # server.sendmail(FROM_EMAIL, user_list[-1], MESSAGE_FORMAT)
#     # server.quit()

#     # time.sleep(30)

# # print user_list
# # print user_list
# user_list = read_email_from_gmail(user_list)

# for i, company in enumerate(company_list):
#     company_list[i]["email"] = user_list[i]
#     prepare_company_paste(company_list[i], copy_emails_file)    

# # print company_list






















