from pwn import *

# Set up the context for the binary
context.binary = './pwn/string/fmt-5/fmt5'
context.arch = 'i386'
context.log_level = 'debug'

# Load the binary
elf = context.binary
