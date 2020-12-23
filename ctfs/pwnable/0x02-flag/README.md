# `flag` #

## Problem Description ##

Papa brought me a packed present! let's open it.

Download : http://pwnable.kr/bin/flag

This is reversing task. all you need is binary

## Initial Analysis ##

First, we download and run the file. That gives us the following:

`I will malloc() and strcpy the flag there. take it.`

Alright, the string is probabaly going to be pretty blatant if we open this file in a debugger. A thing to note is that `malloc()` allocates memory dynamically, which is going to put our flag on the _heap_. We're going to need some way to read the heap.

## Solution ##

Run the binary in `radare2` with `r2 -dA flag`. Do an execution of the binary in the debugger.

Allow the binary to execute once with `dc`. Dump the memory mapping with `dm`. At this point, we expect our flag will be on the heap. `dm` tells us where that is:

```
0x0000000000800000 - 0x0000000000801000 - usr     4K s rwx unk3 unk3
0x0000000001996000 - 0x00000000019b9000 * usr   140K s rw- [heap] [heap]
0x00007fc7a876c000 - 0x00007fc7a876d000 - usr     4K s rw- unk4 unk4
```

From here we'll just enter in the start of the heap (`0x01996000`), enter visual mode, and see if we see something obvious. Eventually we do.

```
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x01998680  0000 0000 0000 0000 0000 0000 0000 0000  ................                                                                                   
0x01998690  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x019986a0  0000 0000 0000 0000 7100 0000 0000 0000  ........q.......
0x019986b0  5550 582e 2e2e 3f20 736f 756e 6473 206c  UPX...? sounds l
0x019986c0  696b 6520 6120 6465 6c69 7665 7279 2073  ike a delivery s
0x019986d0  6572 7669 6365 203a 2900 0000 0000 0000  ervice :).......
```

No Python for this one.