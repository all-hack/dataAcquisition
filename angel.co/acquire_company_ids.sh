# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * * * * * 
# 
#   grab company ids
#   
# 
# 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

page=$1
echo "page: $page"
data="filter_data%5Btab%5D=hiring&filter_data%5Blocations%5D%5B%5D=151282-San+Francisco+Bay+Area&filter_data%5Braised%5D%5Bmin%5D=10000&filter_data%5Braised%5D%5Bmax%5D=100000000&filter_data%5Bsignal%5D%5Bmin%5D=7&filter_data%5Bsignal%5D%5Bmax%5D=10&sort=signal&page=$page"
curl 'https://angel.co/company_filters/search_data' -H 'Origin: https://angel.co' -H 'Accept-Encoding: gzip, deflate, br' -H 'X-CSRF-Token: tcxHdkwAhpTL/vm6vzq9GctTvfOc6BKZ81QLzopN6PoAlwQcayhgskprZ42dgGWtLbZDe4skQP/1XI3q2Sv/Mw==' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: https://angel.co/companies?tab=hiring&locations[]=151282-San+Francisco+Bay+Area&raised[min]=10000&raised[max]=100000000&signal[min]=7&signal[max]=10' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data $data --compressed > id_buff.txt




