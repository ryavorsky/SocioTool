# Retrieve data from VK

import urllib.request
import json
from time import strftime
from datetime import datetime

def retrieve_users():
    reslist = []
    for i in range(1):
        ofs = str(i*1000)
        url_str = "https://api.vk.com/method/groups.getMembers?group_id=auchanrussia&offset="+ofs
        print(url_str)
        res_str = str(urllib.request.urlopen(url_str).read(), encoding="utf-8")
        print(res_str[:100])
        res_data = json.loads(res_str)
        res_array = res_data["response"]["users"]
        reslist = reslist + res_array
    return reslist

    
def user_data(uid):
    url_str = "https://api.vk.com/method/users.get?user_ids="+str(uid) + "&fields=last_seen"
    res_str = str(urllib.request.urlopen(url_str).read(), encoding="utf-8")
    res_data = json.loads(res_str)
    res = res_data["response"][0]
    return res

def last_seen(x):
    return x["last_seen"]["time"]

def timestamp(t):
    return datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')

def main():
    arr = retrieve_users()
    print(len(arr))

    all_user_data = [user_data(user) for user in arr]

    all_user_data.sort(key=last_seen)
    

    for d in all_user_data:
        time = timestamp(last_seen(d))
        print(time)
        
    print(all_user_data)

    res_file=open("auchan.txt", "w")
    for d in all_user_data:
        res_file.write(timestamp(last_seen(d)) + "\t" + str(d)+ "\n")
    res_file.close()
    
main()
