[x] Starting local process './pwn/stack/rop-1/rop1'
[+] Starting local process './pwn/stack/rop-1/rop1': pid 12061
[*] Process './pwn/stack/rop-1/rop1' stopped with exit code -11 (SIGSEGV) (pid 12061)
[x] Parsing corefile...
[*] '/mnt/d/project/LLM4CTF/core.12061'
    Arch:      i386-32-little
    EIP:       0x6261616b
    ESP:       0xffe58120
    Exe:       '/mnt/d/project/LLM4CTF/pwn/stack/rop-1/rop1' (0x8048000)
    Fault:     0x6261616b
[+] Parsing corefile...: Done
[*] EIP is overwritten with: 0x6261616b
[+] Offset found: 140
[*] '/mnt/d/project/LLM4CTF/pwn/stack/rop-1/rop1'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[*] Address of not_called: 0x080484a4
[x] Starting local process './pwn/stack/rop-1/rop1'
[+] Starting local process './pwn/stack/rop-1/rop1': pid 12071
[*] Switching to interactive mode
hello world! Is there a error?
[*] Stopped process './pwn/stack/rop-1/rop1' (pid 12071)

