## babyre

After opening the binary in Ghidra, we can see one interesting part:

![xormekekw](https://i.imgur.com/XhL6Z8h.png)

Looks like the string there is run through an ``xor`` with the key of ``0x17``. Using cyberchef, I am easily able to get the flag.

> IceCTF{e4zy_p33zy_23542}