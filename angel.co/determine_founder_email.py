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

serialized_file = "serialize_companies.txt"
FROM_EMAIL  = os.environ['MAIL_TEST_TRIAL_U'] 
FROM_PWD    = os.environ['MAIL_TEST_TRIAL_P']
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

def read_email_from_gmail(user_list):
    
    email_txt = open("tested_emails.txt", "a")
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        email_check_flag = True

        while len(user_list) > 0:
            user = user_list.pop()
            if email_check_flag == True:
                for i in range(latest_email_id, first_email_id, -1):
                    typ, data = mail.fetch(i, '(RFC822)' )
                    
                    for response_part in data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_string(response_part[1])
                            email_subject = msg['subject']
                            email_from = msg['from']                    
                            if msg['from'] == "Mail Delivery Subsystem <mailer-daemon@googlemail.com>":                                
                                break_out = False
                                while (break_out == False and len(user_list) > 0):
                                    if user == msg["X-Failed-Recipients"]:
                                        email_txt.write("working on it\n")
                                        break_out = True
                                    else:
                                        email_txt.write(user+"\n")
                                        user = user_list.pop()
                                
                    email_check_flag = False
            else:
                print ""
    except Exception, e:
        print str(e)

mail = imaplib.IMAP4_SSL(SMTP_SERVER)
mail.login(FROM_EMAIL,FROM_PWD)
mail.select('inbox')
type, data = mail.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()
first_email_id = int(id_list[0])
latest_email_id = int(id_list[-1])

user_list = []
# user_list.append("oliverbelanger@gmail.com")
# user_list.append("adfoiadf@haoahfoiahd.com")
# user_list.append("adfjaidfj@mmmmmmm.com")
# user_list.append("adfjaidfj@sssss.com")
# user_list.append("obelanger@fordham.edu")

import_file = open(serialized_file, "r")
import_string = import_file.read()
import_lines = import_string.split("\n")

for i, line in enumerate(import_lines[:-1]):
    if line == import_lines[0] or line == import_lines[1]:
        continue
    if i < :
        break

    company = json.loads(line)
    toaddrs = ""

    domain = "".join(company["website"].split("www."))
    domain = "".join(domain.split("https"))
    domain = "".join(domain.split("http"))
    domain = "".join(domain.split("://"))
    domain = "".join(domain.split("/"))
    domain = "".join(domain.split("?utm_source=angellist"))
    domain = "".join(domain.split("?referer=angellist"))

    user = company['founder'].split(" ")[0].lower()    
    user_list.append("{0}@{1}".format(user, domain))    
    
    print "sending email[{0}]: {1}", i, user_list[-1]
    Subj = "holiday property"
    msg = "Hello\n\nwww.Self-catering-breaks.com is now becoming one of the largest sites on the internet\n\nfor people who wish to list their own properties\n\nWe already have 1000's of properties listed but want to make sure you already have\n\nlisted your properties.\n\nSo please feel free to add your property or properties.\n\nFirstly register and you will be emailed an authorisation key.\n\nThanks for your time and please pass this email onto anyone you think may be\n\ninterested to list for free."
    MESSAGE_FORMAT = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" %(FROM_EMAIL, user_list[-1],Subj,msg)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(FROM_EMAIL,FROM_PWD)
    # print user_list
    # server.sendmail(FROM_EMAIL, user_list[-1], MESSAGE_FORMAT)
    server.quit()

    # time.sleep(30)

# print user_list
# read_email_from_gmail(user_list)
























