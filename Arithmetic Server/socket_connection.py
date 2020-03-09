import socket

ip = '127.0.0.1'
port = 7777
version = 0

db_url = "C:/Users/luraw/OneDrive/Desktop/db/"

def data_receive():
    size = 1024
    sever_addrs = (ip, port)

    data = bytearray(b'')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        try:
            c.connect((ip,port))
            print(">> Connect ", ip)

            c_msg = bytes("client_ready\n", 'UTF-8')
            ## '\n' 빠트리지 않게!!, 데이터 받을 때 끝을 표시하는거 잊지말기.

            c.send(c_msg) #client ready

            s_msg = c.recv(1024).decode() #sever ready

            if s_msg == "server_ready":
                print("\n>> server_ready")
                c.send(bytes("client_ACK\n", 'UTF-8'))

                print("\n>> down start")

                with open(db_url, mode="a", encoding='utf8',errors = 'ignore') as f:
                    while True:
                        data = c.recv(1024).decode(errors='ignore')

                        if data.find("!download_end") != -1:
                            data = data.replace("!download_end", "")
                            f.write(data)
                            print(" \n>> download end")
                            break

                        f.write(data)

        except Exception as e:
            print(e)
    
    return data

