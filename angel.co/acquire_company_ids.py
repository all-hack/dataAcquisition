#!/usr/bin/env python
import sys
import requests
import pprint
import glob
import time

pp = pprint.PrettyPrinter(indent=4)

page = 3
# while (1)
# try:

# curl 'https://angel.co/company_filters/search_data' 
# -H 'Cookie: mp_6a8c8224f4f542ff59bd0e2312892d36_mixpanel=%7B%22distinct_id%22%3A%20%221467558%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22%24username%22%3A%20%22oliver-belanger%22%2C%22angel%22%3A%20false%2C%22candidate%22%3A%20false%2C%22roles%22%3A%20%5B%0A%20%20%20%20%22full%20stack%20developer%22%2C%0A%20%20%20%20%22consultant%22%0A%5D%2C%22quality_ceiling%22%3A%20%224%22%7D; _ga=GA1.2.202711447.1490389020; _gid=GA1.2.431933958.1500408949; _gat=1; ajs_group_id=null; ajs_user_id=%221467558%22; ajs_anonymous_id=%22d87a68a4d89dd776bcfa0a90b62c6759%22; amplitude_idangel.co=eyJkZXZpY2VJZCI6IjNmZTFjMDhhLTIwOWEtNDQ4OS05Yzc2LWUxN2NhMjZmNjY5MVIiLCJ1c2VySWQiOiIxNDY3NTU4Iiwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNTAwNDMxNDkwMTYwLCJsYXN0RXZlbnRUaW1lIjoxNTAwNDMyMDE3OTUwLCJldmVudElkIjoyMiwiaWRlbnRpZnlJZCI6NTgsInNlcXVlbmNlTnVtYmVyIjo4MH0=; _angellist=ad02d439022bbb42928b48b798bebd50' 
# -H 'Origin: https://angel.co' 
# -H 'Accept-Encoding: gzip, deflate, br' 
# -H 'X-CSRF-Token: tcxHdkwAhpTL/vm6vzq9GctTvfOc6BKZ81QLzopN6PoAlwQcayhgskprZ42dgGWtLbZDe4skQP/1XI3q2Sv/Mw==' 
# -H 'Accept-Language: en-US,en;q=0.8' 
# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' 
# -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' 
# -H 'Accept: */*' 
# -H 'Referer: https://angel.co/companies?tab=hiring&locations[]=151282-San+Francisco+Bay+Area&raised[min]=10000&raised[max]=100000000&signal[min]=7&signal[max]=10' 
# -H 'X-Requested-With: XMLHttpRequest' 
# -H 'Connection: keep-alive' 
# --data 'filter_data%5Btab%5D=hiring&filter_data%5Blocations%5D%5B%5D=151282-San+Francisco+Bay+Area&filter_data%5Braised%5D%5Bmin%5D=10000&filter_data%5Braised%5D%5Bmax%5D=100000000&filter_data%5Bsignal%5D%5Bmin%5D=7&filter_data%5Bsignal%5D%5Bmax%5D=10&sort=signal&page=2' --compressed


headers = {
    'Cookie': 'mp_6a8c8224f4f542ff59bd0e2312892d36_mixpanel=%7B%22distinct_id%22%3A%20%221467558%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22%24username%22%3A%20%22oliver-belanger%22%2C%22angel%22%3A%20false%2C%22candidate%22%3A%20false%2C%22roles%22%3A%20%5B%0A%20%20%20%20%22full%20stack%20developer%22%2C%0A%20%20%20%20%22consultant%22%0A%5D%2C%22quality_ceiling%22%3A%20%224%22%7D; _ga=GA1.2.202711447.1490389020; _gid=GA1.2.431933958.1500408949; ajs_group_id=null; ajs_user_id=%221467558%22; ajs_anonymous_id=%22d87a68a4d89dd776bcfa0a90b62c6759%22; amplitude_idangel.co=eyJkZXZpY2VJZCI6IjNmZTFjMDhhLTIwOWEtNDQ4OS05Yzc2LWUxN2NhMjZmNjY5MVIiLCJ1c2VySWQiOiIxNDY3NTU4Iiwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNTAwNDE3NTAzNzE3LCJsYXN0RXZlbnRUaW1lIjoxNTAwNDE3NTAzNzIxLCJldmVudElkIjoyMiwiaWRlbnRpZnlJZCI6NTYsInNlcXVlbmNlTnVtYmVyIjo3OH0=; _angellist=ad02d439022bbb42928b48b798bebd50',
    'Origin': 'https://angel.co',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-CSRF-Token': 'tcxHdkwAhpTL/vm6vzq9GctTvfOc6BKZ81QLzopN6PoAlwQcayhgskprZ42dgGWtLbZDe4skQP/1XI3q2Sv/Mw==',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Referer': 'https://angel.co/companies?tab=hiring&locations[]=151282-San+Francisco+Bay+Area&raised[min]=10000&raised[max]=100000000&signal[min]=7&signal[max]=10',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
}
payload = {
    'data': "filter_data%5Btab%5D=hiring&filter_data%5Blocations%5D%5B%5D=151282-San+Francisco+Bay+Area&filter_data%5Braised%5D%5Bmin%5D=10000&filter_data%5Braised%5D%5Bmax%5D=100000000&filter_data%5Bsignal%5D%5Bmin%5D=7&filter_data%5Bsignal%5D%5Bmax%5D=10&sort=signal&page={0}".format(page)
}
url = 'https://angel.co/company_filters/search_data'
r = requests.get(url, headers=headers, data=payload)

f = open("company_ids.txt", "a")

print r.json()['ids']

for ed in r.json()['ids']:
    f.write(str(ed))

page += 1
if r.json()['ids']:
    print "gooo"
time.sleep(60)
# except:
    # break

























































