# Collision #

## Problem Description ##

```
Daddy told me about cool MD5 hash collision today.
I wanna do something like that too!

ssh col@pwnable.kr -p2222 (pw:guest)
```

## Reconnaissance and Analysis ##

As before, logging in we see some files in the home directory.

```
root@kali:collision# ssh col@pwnable.kr -p2222
col@pwnable.kr's password: 
col@ubuntu:~$ ls
col  col.c  flag
```

Read out `col.c` and see what we're looking at.

```c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}
```

Our hint is that this has something to do with hash collision. The passcode must be 20 bytes long. `argv[1]` (the argument given to `col`) is checked for a 20 byte length, then `check_password()` is run on that argument.

The argument gets cast as an integer and then the five digits of this integer are summed into a result. The result is then compared to `hashcode`. If they're equal, we win.

## Solution ##

From the code, `hashcode=0x21DD09EC`, or 568134124 in decimal.

Here, characters we use in `argv[1]` become one byte and integers are four bytes. The passcode must be twenty bytes. So, we need five integers that sum to 568134124. Our "inject string" (the argument we will supply to the program to capture the flag) is going to have a format like so:

```
aaaabbbbccccddddeee
```

where `aaaa`, `bbbb`, `cccc`, `dddd`, and `eeee` are four-byte values that sum to `0x21DD09EC`. It's not perfectly divisible by 5, so we could use `0x6C5CEC8` four times and `0x06C5CECC` for the fifth value. For the mathematically challenged 

These aren't typeable characters, so we could achieve injection in the command line using a `perl` command, like so.

`./col $(perl -e 'print "\xc8\xce\xc5\x06"x4 . "\xcc\xce\xc5\x06"')`

Note that a char has two hex "numbers" associated with it (for example, `0x00` is a `null` char) and that the bytes are arranged little-endian. 

## Concepts and Further Reading ##

## `pwntools` Implementation ##

The `pack()` function within `pwntools` proves handy here.

```python
from pwn import *

# Connect to the target. #
r = ssh(host='pwnable.kr',
        user='col',
        password='guest',
        port=2222)

# Craft our bad input #
payload = pack(0x6c5cec8)*4 + pack(0x6c5cecc)

# Run the target binary with the payload. #
p = r.process(['col',payload])

# Collect the output #
output = p.recvall()
print(output)
```