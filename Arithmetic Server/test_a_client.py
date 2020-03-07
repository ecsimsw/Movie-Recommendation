import socket

def data_read_by_socket():
    # 접속 정보 설정
    ip = '127.0.0.1'
    port = 8080
    size = 1024
    sever_addrs = (ip, port)

    data = bytearray(b'')

    # 클라이언트 소켓 설정
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect(sever_addrs) 
        
        c.send('client_ready'.encode())
        
        while True:
            data = c.recv(size)  
            if data != None:
                break
                
        if data == b"server_ready":
            f_size = c.recv(1024)
            c.send("c_ack".encode())
            
            print("=== file down loading ===")
            with open('C:/Users/luraw/OneDrive/Desktop/db/saved.csv', 'w', encoding="UTF-8") as f:
                data = c.recv(int(f_size.decode()))
                f.write(data.decode())
        
        print('데이터 수신: {}'.format(str(data)))     
    return data


a = data_read_by_socket()

print(a)