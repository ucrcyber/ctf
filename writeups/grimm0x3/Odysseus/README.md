
## Odysseus - 500 Points 

> I already encrypted the flag once but two times can never hurt right? I'll let you send me another key to encrypt it with! (in hex)

Based on the description, this challenge requires a DES Weak Key Attack. Weak keys are keys that cause the encryption to act identically to the decryption mode.

I used the list of keys [found on this github repo](https://github.com/W3rni0/NahamCon_CTF_2020/blob/master/assets/files/keys). Simple pwntools script to get the flag:

```
from pwn import *

#nc challenge.ctf.games 32350

with open('keys') as my_file:
    keys_array = my_file.readlines()


for key in keys_array:
        conn = remote('challenge.ctf.games', 32350)
        conn.recvline()
        conn.send(key)
        try:
                hex_string = str(conn.recvline(), 'utf-8')[1:-1]
                bytes_object = bytes.fromhex(hex_string)
                ascii_string = bytes_object.decode("ASCII")
                print(ascii_string)
                if flag in ascii_string:
                        exit(1)
        except:
                pass
        conn.close()
```

> flag{9b9169ac15fe51e8f337bc2786e4fb36}