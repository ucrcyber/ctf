from pwn import *

#nc challenge.ctf.games 32350

with open('keys') as my_file:
    keys_array = my_file.readlines()


for key in keys_array:
        conn = remote('challenge.ctf.games', 32350)
        conn.recvline()
        conn.send(key)
        try:
                hex_string = str(conn.recvline(), 'utf-8')[1:-1]
                bytes_object = bytes.fromhex(hex_string)
                ascii_string = bytes_object.decode("ASCII")
                print(ascii_string)
                if flag in ascii_string:
                        exit(1)
        except:
                pass
        conn.close(