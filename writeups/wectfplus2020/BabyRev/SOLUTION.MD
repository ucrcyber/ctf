## Baby Rev - 39 Solves

> Shou only allows his gay friends to view the flag here. We got intels that he used PHP extension for access control and we retrieved a weird binary.

In this challenge, we are given a compiled binary file. I used ``Ghidra`` to decompile it. After looking around, I noticed some interesting decompiled code in the ``ziv waf echo`` function.

```
  puVar2 = (ulong *)zend_hash_str_find(*(undefined8 *)(param_1 + 0x50),"HTTP_USER_AGENT",0xf);
  if (puVar2 == (ulong *)0x0) {
LAB_00101262:
    php_printf("Unauthorized Visit\n");
  }
  else {
    lVar3 = 0x10;
    bVar8 = 0xffffffffffffffe7 < *puVar2;
    pbVar4 = (byte *)(*puVar2 + 0x18);
    bVar9 = pbVar4 == (byte *)0x0;
    pbVar5 = (byte *)"Flag Viewer 2.0";
    do {
      if (lVar3 == 0) break;
      lVar3 = lVar3 + -1;
      bVar8 = *pbVar4 < *pbVar5;
      bVar9 = *pbVar4 == *pbVar5;
      pbVar4 = pbVar4 + (ulong)bVar10 * -2 + 1;
      pbVar5 = pbVar5 + (ulong)bVar10 * -2 + 1;
    } while (bVar9);
    if ((!bVar8 && !bVar9) != bVar8) goto LAB_00101262;
    php_printf(&DAT_00102020,uVar6,local_38 + 0x18);
  }
  *(undefined4 *)(param_2 + 8) = 3;
  ```

The thing that sticks out to be here is ``HTTP_USER_AGENT``. A user agent is like an identifier for a browser. Looking at the variable ``puVar2``, it is set equal to ``puVar4`` which is then compared to ``puVar5``. ``puVar5`` contains the string ``"Flag Viewer 2.0"``. Since this is a baby challenge, you can make the assumption that the challenge is not too complicated, and guess that this needs to be your user agent string. You can use the tool curl to request the web page with specified user agent, and get the flag.

```
curl -A "Flag Viewer 2.0" http://babyrev.ny.ctf.so/
```

```
we{e1a39122-6c82-4e09-8e84-d3a55dc28cca@fr3e_r3v-1n-w3bc7f!}
```
