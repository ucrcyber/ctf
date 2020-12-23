# `bof` #

## Challenge Text ##

Nana told me that buffer overflow is one of the most common software vulnerability. 
Is that true?

Download : http://pwnable.kr/bin/bof
Download : http://pwnable.kr/bin/bof.c

Running at : nc pwnable.kr 9000

## Initial Analysis ##

Clearly, this wants us to do a buffer overflow. Somehow we're meant to use a buffer overflow to overwrite a key value. However, putting in an arbitrarily long input gets us the following.

```
$ ./bof                                                                             
overflow me : 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Nah..
*** stack smashing detected ***: terminated
zsh: abort      ./bof
```

So, [stack smashing protection](https://wiki.osdev.org/Stack_Smashing_Protector) has been enabled. Most likely this is manifesting as some kind of canary value. If we overflow the buffer, we will overwrite the canary. If we overwrite the canary, the program will halt. Sometimes it's just some arbitrary secret. Other times, it's special characters that terminate the string.

Looking at the source code, which is helpfully provided:

```
void func(int key){
        char overflowme[32];
        printf("overflow me : ");
        gets(overflowme);       // smash me!
        if(key == 0xcafebabe){
                system("/bin/sh");
        }
        else{
                printf("Nah..\n");
        }
}
```

Our buffer is a 32 byte variable named `overflowme`. This needs to eventually overflow into `key`, to change its value to `0xcafebabe`.

## Naive Solution ##

It's possible that the stack overflow protection is poor. We can attempt to brute force the solution by adding the target string to the end of an arbitrarily long string, keeping in mind that the string needs to be written little endian. For example:

`payload = 'a'*n + '\xbe\xba\xfe\xca'`

Running a brute force as per `bof_solution.py`, there isn't actually any effective stack canary protection. In the real world there would be, but this is supposed to be the easy stuff. The solution eventually resolves at `n=52`. Transmitting this to the server, we can obtain a shell and, by extension, the flag.

After we exit the interactive shell, the bof binary encounters our stack smash a bit too late.

## Explaination ##

TODOs

### Initial Survey / Static Analysis

I perform my binary analysis for this in `radare2`.

Open the binary in radare2 with `r2 -dAA bof`. We can get the layout of the main function with `pdf@main` and see that it's calling a function, called `sym.func` in `radare2`, that is performing the comparison. 

From within `pdf@sym.func` we'll see the comparison to `0xcafebabe` at memory location `0x00000654`, and a `__stack_chk_fail` call at `0x00000683`.

We'll have to run this binary and see what the stack looks like, what canary values are being put in place.
