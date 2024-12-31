from pwn import *

# Set up the context for 32-bit ELF
context(arch='i386', os='linux')

# Define the binary and the remote or local connection
binary = './pwn/stack/rop-2/rop2'

# Start the process
p = process(binary)
