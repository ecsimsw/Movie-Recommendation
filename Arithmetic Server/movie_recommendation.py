import csv

import filter
import get_value
import scoring

import socket

meta_file_url_D = "C:/Users/luraw/OneDrive/Desktop/data/movies_metadata.csv"
meta_file_url_L = "C:/Users/user/Desktop/data/test_meta.csv"

rating_file_url_D = "C:/Users/luraw/OneDrive/Desktop/data/test_ratings.csv"
rating_file_url_L = "C:/Users/user/Desktop/data/test_ratings.csv"

def temp_db_load(url):
    data_file =[]

    with open(url, mode='r', encoding='utf8', errors='ignore') as f:
        csv_ = csv.reader(f)
        for i in csv_:
            data_file.append(i)
        return data_file

def recommend(search, data_file, n):
    # search : 찾을 영화를 웹에서 입력해서 전달 받을 것
    # data_file = 영화 메타 데이터 정보를 DB에서 전달 받을 것
    # n : 추천할 영화 개수를 메인 서버에서 결정해서 전달 받을 것

    # return : 추천할 n개의 영화

    print("search : ",get_value.title(search))

    data = data_file[1:]

    index = input("search movie index : ")
    search = data[int(index)]

    search_list = []
    search_list.append(search)

    ## 데이터에서 검색군 제거
    candidates = filter.sub_list(data, search_list)

    ## 필터로 언어, 시리즈, 장르 유사를 확인
    selected, candidates = filter.stream_filter(search,candidates, n)

    n = n - len(selected)
    score_list = []

    ## 필터에서 선택된 선택군의 내용 유사 점수를 계산하여 추가

    overview_search = get_value.overview(search)
    s_overview_smi = scoring.similarites(overview_search, get_value.get_overviews(selected))

    for smi in s_overview_smi:
        score_list.append(smi)

    ## 남은 후보군을 내용 유사도 계산 후 선택군에 추가

    overview_candidates =get_value.get_overviews(candidates)
    overview_smi = scoring.similarites(overview_search, overview_candidates)

    ## 점수를 기준으로 정렬하여 선택군에 추가

    c_overview_smi = []
    for index in range(len(candidates)):
        temp = (index,overview_smi[index])
        c_overview_smi.append(temp)

    sorted_c_overview_smi = sorted(c_overview_smi, key = lambda x : x[1], reverse =True)

    for lot in range(n):
        score_list.append(sorted_c_overview_smi[lot][1])
        selected.append(candidates[lot])

    ## 반환은 선택군과, 점수표를 반환
    return selected, score_list

data_temp = temp_db_load(meta_file_url_D)
recommend("search", data_temp, 10)

def data_read_by_socket():
    HOST = '127.0.0.1'
    PORT = 9999

    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

    client_socket.connect((HOST, PORT)) 

    # 키보드로 입력한 문자열을 서버로 전송하고 

    # 서버에서 에코되어 돌아오는 메시지를 받으면 화면에 출력합니다. 

    # quit를 입력할 때 까지 반복합니다. 
    
    while True: 

        message = input('Enter Message : ')
        if message == 'quit':
            break

        client_socket.send(message.encode()) 
        data = client_socket.recv(1024) 

        print('Received from the server :',repr(data.decode())) 


    client_socket.close() 
