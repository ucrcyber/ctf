## My Hometown

> I love my hometown, why hide it?

Starting off, we are given an image that looks like a movie cover. I reverse image searched it and that it corresponded to the comedy ``Eurovision Song Contest: The Story of Fire Saga``.

From the search results from the reverse image search, I could see several articles mentioning that the comedy was filmed in ``Husavik``, or has something to do with ``Husavik``. As the image is a ``jpg`` file, I was able to use the tool ``steghide`` to extract data from the image with the password ``Husavik``.

```
steghide extract -sf fs.jpg
```

Doing this and entering ``Husavik`` as the password, we are given the file ``secret.txt``. Here are the contents:

```python
n = 147767851294746620911810388038107728286037238915263678277473972113895902805449170503702649265216615588582242631818941986820754345835910513454492874669403644985033217666215892611622964797736512917384094418165479541796699940155391259232322549057354995706147434748297162590026274856168980580303832087722706212591
c = pow(bytes_to_long(m),3,n)
print(c)
#c = 748581664569261393653185381818017922717194231102617050589231695775701708792363247054972885709293669476065709136086780761429082534333192111209529254996467657486910468154090043100616141793324960308559815737581366862445109973777659037057000L
```

!!! Fun. It looks like we need to find ``m``, and to do so we would have to reverse the function ``pow(a, b, c)``. Sounds simple enough? Except that the third parameter ``c`` is mod, which is not reversable.

I found [this stackoverflow thread](https://stackoverflow.com/questions/49818392/how-to-find-reverse-of-powa-b-c-in-python) which mentioned that reversing this is similar to an RSA problem. Following the logic laid out in the post, I was able to convert the data we have to the following numbers:

```
n = 147767851294746620911810388038107728286037238915263678277473972113895902805449170503702649265216615588582242631818941986820754345835910513454492874669403644985033217666215892611622964797736512917384094418165479541796699940155391259232322549057354995706147434748297162590026274856168980580303832087722706212591
e = 3
c = 748581664569261393653185381818017922717194231102617050589231695775701708792363247054972885709293669476065709136086780761429082534333192111209529254996467657486910468154090043100616141793324960308559815737581366862445109973777659037057000
```

And now we have the form of a classic RSA problem. The exponent ``e`` is really small, so it is vulnerable to a small exponent attack.

I was able to take the following steps to solve for the plaintext ``m``. After that, I run ``long_to_bytes`` to reverse the function in the code above.

![bigbrainshit](https://i.imgur.com/buG0I20.png)

We are given a base64 string which decodes into coordinates.

```
64.0334627,-21.9000902
```

I was stuck with what to do at this point as they point to a town in Iceland. After asking the organizers, the flag is physically at those coordinates. Since I do not live anywhere near Iceland (and neither do several of the CTF players) we were given the option to submit a festive photo of the team in exchange for the flag. 

> IceCTF{hometown_holiday_photo_op_special}