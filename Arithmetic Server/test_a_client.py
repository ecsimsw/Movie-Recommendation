import socket

def data_read_by_socket():
    # 접속 정보 설정
    ip = '127.0.0.1'
    port = 7777
    size = 1024
    sever_addrs = (ip, port)

    data = bytearray(b'')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        try:
            c.connect((ip,port))
            print("Connect ", ip)

            c_msg = bytes("client_ready\n", 'UTF-8')
            ## '\n' 빠트리지 않게, 서버에서 \n을 기다린다.

            c.send(c_msg)

            s_msg = c.recv(1024).decode()

            if s_msg == "server_ready":
                print("\n=== server_ready ===")
                c.send(bytes("client_ACK\n", 'UTF-8'))

                print("\n=== down start ===")

        except Exception as e:
            print(e)
    
    return data


result = data_read_by_socket()

#print(a)