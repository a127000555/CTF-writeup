# CTF hw4
> b05902127 劉俊緯, user ID: a127000555

> FLAG{g0_b1n4ry_1s_pmu4d13_bnT_n0t_Th4t_34sy_QQ}

## Routine

* file: It's x64.

  ![1542238999639](/home/arvin/.config/Typora/typora-user-images/1542238999639.png)

* checksec : We can bof the return address.

![1542238047504](/home/arvin/.config/Typora/typora-user-images/1542238047504.png)

* strace : syscall: read/write

![1542238335946](/home/arvin/.config/Typora/typora-user-images/1542238335946.png)

* Conclustion:
  * No  canary -> easy to ROP。
  * read&write -> use buffer to overwrite。

## Setting ROP Chain

* To get shell:
| %rax | System call | %rdi                 | %rsi                     | %rdx                     |
| ---- | ----------- | -------------------- | ------------------------ | ------------------------ |
| 59   | sys_execve  | const char *filename | const char *const argv[] | const char *const envp[] |
| 0x3b |             | pointer to '/bin/sh' | 0                        | 0                        |
* set up rdi:
  * to load pointer that save something, we must find gadget with "mov qword ptr" or "mov ???, rsp" to get.
  * gadget: "mov qword ptr [rdi], rax ; ret"
    * Which must let rax be '/bin/sh' with zero end (\x00).
  * so, we pop rax + b"/bin/sh" to let rax = '/bin/sh'.
* set rdx:
  * gadget : "pop rdx; or dh,dh; ret"
  * value: 0x00
* set rsi:
  * gadget : "pop rsi; ret" is not exist, we use the most similar form: "movsxd rsi, eax ; ret"
    * Which must clear the eax first.
      * gadget:  "pop rax; ret" with value 0x00
  * value: 0x00
* set up rax:
  - gedget : "pop rax; ret"
  - value: 0x3b
* call syscall:
  * gadget: "syscall"

## Find Offset

* First, randomlly poke goto with some string.

* Well, it's not a difficult task because go's error handling tells everything.

![1542463885387](/home/arvin/.config/Typora/typora-user-images/1542463885387.png)

* because fp is: 0xc420059f88, 

  * So ret address is in  0xc420059f80.

  ![1542469799913](/home/arvin/.config/Typora/typora-user-images/1542469799913.png)

* And we find the string is start from 0xc420059e38.
* 0xc420059f80-0xc420059e38 = 328 = the trash we put.

* However, we'll still get the error message that "malloc with too large memory", we use 'a' substituation with '\x00' to avoid malloc error.