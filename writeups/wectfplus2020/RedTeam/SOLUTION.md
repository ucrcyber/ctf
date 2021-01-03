
## Red Team - 62 Solves

> We overheard that Shou's company hoarded a shiny flag at a super secret subdomain. His company's domain: shoustinycompany.cf Note: You are allowed to use subdomain scanner in this challenge.


Ok, we are given a website and we have to find a subdomain with the flag. We are not allowed to use tools like dirbuster or burpsuite to brute-force for the subdomain ourself, so we would have to find the subdomain in some other way.

### Normal Solution
I tried to do this using the tool ``dig``, externally from my VM without any luck.

I was following this blog post where I got stuck: https://securitytrails.com/blog/dns-enumeration

After this, I noticed the note that we are allowed to use a ``subdomain scanner``. 

I used this tool: https://pentest-tools.com/information-gathering/find-subdomains-of-domain#

We find two subdomains:

```
ns1.shoustinycompany.cf
docs.shoustinycompany.cf
```

``ns1`` refers to a nameserver (meaning there will be no HTTP server off that subdomain, it can only be used for DNS queries) so we can ignore that subdomain for now. I went to ``docs`` and found the following information:

```
### Company's websites


Looking Glass: lookingglassv1.shoustinycompany.cf

Flag: [Removed by Shou]
```

Going to the lookingglass subdomain, we are taken to a webpage with the option to run the IP and DIG commands against the local server. Since the goal is to find subdomains, I googled for a way to do this Dig.

I found this Stack Overflow Post: https://stackoverflow.com/questions/131989/how-do-i-get-a-list-of-all-subdomains-of-a-domain

Using this query on the website: 

```
dig @ns1.shoustinycompany.cf shoustinycompany.cf axfr
```

Produces the following output:

```
Executed
dig @ns1.shoustinycompany.cf shoustinycompany.cf axfr
Result:

; <<>> DiG 9.14.12 <<>> @ns1.shoustinycompany.cf shoustinycompany.cf axfr
; (1 server found)
;; global options: +cmd
shoustinycompany.cf. 100 IN SOA ns1.shoustinycompany.cf. root.shoustinycompany.cf. 2 604800 86400 2419200 604800
shoustinycompany.cf. 100 IN NS ns1.shoustinycompany.cf.
shoustinycompany.cf. 100 IN A 142.93.28.144
docs.shoustinycompany.cf. 100 IN A 142.93.28.144
lookingglassv1.shoustinycompany.cf. 100 IN A 161.35.126.226
ns1.shoustinycompany.cf. 100 IN A 142.93.28.144
rea11ysu9erse3retsubd0ma1n00000.shoustinycompany.cf. 100 IN A 142.93.28.144
shoustinycompany.cf. 100 IN SOA ns1.shoustinycompany.cf. root.shoustinycompany.cf. 2 604800 86400 2419200 604800
;; Query time: 75 msec
;; SERVER: 142.93.28.144#53(142.93.28.144)
;; WHEN: Sun Dec 20 00:12:37 UTC 2020
;; XFR size: 8 records (messages 1, bytes 303)
```

### Cheese Solution

The following solution as not intended, and upon mentioning it to one of the organizers the challenge was changed so that this would not work.

Using this [website](https://www.nmmapper.com/sys/tools/subdomainfinder/), I was able to find the flag subdomain directly: ``su9erse3retsubd0ma1nucantf1ndlollllll.shoustinycompany.cf``.

```
we{be5620ad-20b5-4dc4-b4fd-a7a0246028e4@1_h0pe_u_l3arnt_ax7r}
```