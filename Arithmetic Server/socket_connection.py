import socket

version = 0
size = 1024
data = bytearray(b'')

def connect(ip, port):
    client_socket =None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip,port))
        print(">> Connect ", ip)

        c_msg = bytes("client_ready\n", 'UTF-8')
        ## '\n' 빠트리지 않게!!, 데이터 받을 때 끝을 표시하는거 잊지말기.

        client_socket.send(c_msg) #client ready

        s_msg = client_socket.recv(1024).decode() #sever ready

        if s_msg == "server_ready":
            print("\n>> server_ready")
            client_socket.send(bytes("client_ACK\n", 'UTF-8'))

    except Exception as e:
        client_socket.close()
        return None

    return client_socket

def file_receive(client_socket, db_url):
    try:
        print("\n>> down start")
        client_socket.send(bytes("down_start\n", 'UTF-8'))

        with open(db_url, mode="w", encoding='utf8',errors = 'ignore') as f:
            while True:
                data = client_socket.recv(1024).decode(errors='ignore')

                if data.find("!download_end") != -1:
                    data = data.replace("!download_end", "")
                    f.write(data)

                    print(" \n>> download end")
                    break

                f.write(data)

    except Exception as e:
        print(e)
        return None

    return db_url

def send_result_lines(client_socket, lines):
    msg_send(client_socket,"send_result")

    for i in lines:
        msg_send(client_socket,i)
    
    msg_send(client_socket, "!download_end")

def msg_receive(client_socket):
    while True:
        s_msg = client_socket.recv(1024).decode()
        if s_msg != "":
            break

    print("rcved : ",s_msg)
    return s_msg

def msg_send(client_socket, msg):
    c_msg = bytes(msg+"\n", 'UTF-8')
    ## '\n' 빠트리지 않게!!, 데이터 받을 때 끝을 표시하는거 잊지말기.
    client_socket.send(c_msg)

def socket_close(client_socket):
    client_socket.close()
    client_socket= None
    print("socket close")