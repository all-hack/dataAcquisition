#!/usr/bin/env python
import sys
import requests
import pprint
import glob
import time
import json
from subprocess import call, check_output
pp = pprint.PrettyPrinter(indent=4)


dir_name = "company_triage"

for page in range(1, 10):
    dir_path = check_output("pwd")[:-1]
    acquire_company_ids_command = "sh {0} {1}".format(str(dir_path+"/"), page)

    call(["mkdir", dir_name])
    call(["sh", "acquire_company_ids.sh", str(page)])

    id_buff = open("id_buff.txt", 'r')
    id_strings = id_buff.read()

    id_json = json.loads(id_strings)

    companie_ids = "ids%5B%5D={0}".format(id_json["ids"][0])
    for i, ed in enumerate(id_json["ids"]):
        if i == 0:
            continue
        else:
            companie_ids += "&ids%5B%5D={0}".format(ed)

    total = str(id_json["total"])
    hexdigest = str(id_json["hexdigest"])

    call(["sh", "acquire_company_info.sh", str(page), companie_ids, total, hexdigest, dir_name])

    id_buff.close()
    time.sleep(20)























