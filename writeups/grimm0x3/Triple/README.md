
## Triple (50 Points)

> I was studying something called ASCII armor because I wanted to become better at encoding. I was having fun until I realized I couldn't decode my message... 

I simply noticed the string encoded in base64 and decoded the string three times.

```
kali@kali:~/Desktop/ctf/grimcon0x3/desshit$ echo V20xNGFGb3pjM3BQVkd0M1RsZFJlVTFVVVRSYWFsSnRXa2RKTTFscVFYbE9WMDE1VFRKUk1rOUVVWGROUkU1cVdXNHdQUT09 | base64 -d | base64 -d | base64 -d
flag{39905d2148f4fdb7b025c23d684003cb}
```

> flag{39905d2148f4fdb7b025c23d684003cb}