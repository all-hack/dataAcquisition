# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * 
# 
#   grab company info
#   
# 
# 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

angel_profile=$1

curl $angel_profile -H 'If-None-Match: W/"1263d63183ef2d445ee3d9b24bd8fd22"' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://angel.co/particle/activity' -H 'Cookie: mp_6a8c8224f4f542ff59bd0e2312892d36_mixpanel=%7B%22distinct_id%22%3A%20%221467558%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22%24username%22%3A%20%22oliver-belanger%22%2C%22angel%22%3A%20false%2C%22candidate%22%3A%20false%2C%22roles%22%3A%20%5B%0A%20%20%20%20%22full%20stack%20developer%22%2C%0A%20%20%20%20%22consultant%22%0A%5D%2C%22quality_ceiling%22%3A%20%224%22%7D; _ga=GA1.2.202711447.1490389020; _gid=GA1.2.1399341080.1500594840; ajs_group_id=null; ajs_user_id=%221467558%22; ajs_anonymous_id=%22d87a68a4d89dd776bcfa0a90b62c6759%22; amplitude_idangel.co=eyJkZXZpY2VJZCI6IjNmZTFjMDhhLTIwOWEtNDQ4OS05Yzc2LWUxN2NhMjZmNjY5MVIiLCJ1c2VySWQiOiIxNDY3NTU4Iiwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNTAwNjI5ODg5NDk1LCJsYXN0RXZlbnRUaW1lIjoxNTAwNjMxNDM0NDE4LCJldmVudElkIjoyMiwiaWRlbnRpZnlJZCI6OTMsInNlcXVlbmNlTnVtYmVyIjoxMTV9; _angellist=ad02d439022bbb42928b48b798bebd50' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed > "profile_buff.txt"




