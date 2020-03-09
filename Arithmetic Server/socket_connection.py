import socket

ip = '127.0.0.1'
port = 7777
version = 0
size = 1024
data = bytearray(b'')

test_db_url = "C:/Users/luraw/OneDrive/Desktop/db/meta_data.csv"

sever_addrs = (ip, port)
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
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

    except Exception as e:
        print(e)
        c.close()
        return False

    return True

def file_receive(db_url = test_db_url):
    rcv_file = []
    try:
        print("\n>> down start")
        c.send(bytes("down_start\n", 'UTF-8'))

        with open(db_url, mode="a", encoding='utf8',errors = 'ignore') as f:
            while True:
                data = c.recv(1024).decode(errors='ignore')

                if data.find("!download_end") != -1:
                    data = data.replace("!download_end", "")
                    f.write(data)
                    rcv_file.append(data)

                    print(" \n>> download end")
                    break

                f.write(data)
                rcv_file.append(data)

    except Exception as e:
        print(e)
        return None

    return db_url

def send_result_lines(lines):
    msg_send("send_result")

    for i in lines:
        msg_send(i)
    msg_send("!download_end")

def msg_receive():
    s_msg = c.recv(1024).decode()

    return s_msg

def msg_send(msg):
    c_msg = bytes(msg+"\n", 'UTF-8')
    ## '\n' 빠트리지 않게!!, 데이터 받을 때 끝을 표시하는거 잊지말기.
    c.send(c_msg)

def socket_close():
    c.close()
    print("socket close")

"""
##test 

lines = []

string = "1.Sudden Death\
languages : en\
genres : Action, Adventure, Thriller\
companies : Universal Pictures, Imperial Entertainment, Signature Entertainment\
overview : International action superstar Jean Claude Van Damme teams with Powers Boothe in a Tension-packed, suspe\
during a championship hockey game. With the captors demanding a billion dollars by games end, Van Damme frantically\
vote_ave : 5.5"

for i in range(10):
    lines.append(string)

connect()
file_receive()

title = msg_receive()

send_result_lines(lines)
"""