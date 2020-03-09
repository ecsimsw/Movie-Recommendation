import csv

import filter
import get_value
import scoring

import socket

rcv_file_url_L = "C:/Users/user/Desktop/data/get.csv"

def file_load(url):
    data_file =[]

    with open(url, mode='r', encoding='utf8', errors='ignore') as f:
        csv_ = csv.reader(f)
        for i in csv_:
            data_file.append(i)
        return data_file

def input_title_to_search(search_title,data_movies):
    search_index = -1

    for index in range(len(data_movies)):
        if search_title == get_value.title(data_movies[index]):
            search_index = index
            return data_movies[index]

    if search_index == -1:
        print("No data")
        return None
        ## 영화가 데이터에 없음 
    
def recommend(search, data_movies, n, Mode= "G"):
    # search : 찾을 영화를 웹에서 입력해서 전달 받을 것
    # data_file = 영화 메타 데이터 정보를 DB에서 전달 받을 것
    # n : 추천할 영화 개수를 메인 서버에서 결정해서 전달 받을 것
    # return : 추천할 n개의 영화

    data = data_movies

    search_list = []
    search_list.append(search)

    ## 데이터에서 검색군 제거
    candidates = filter.sub_list(data, search_list)

    ## 필터로 언어, 시리즈, 장르 유사를 확인
    if Mode == "G":
        selected, candidates = filter.stream_filter(search,candidates, n)
    else:
        selected, candidates = filter.stream_filter_withoutGenre(search,candidates, n)

    n = n - len(selected)
    score_list = []

    ## 필터에서 선택된 선택군의 내용 유사 점수를 계산하여 추가

    overview_search = get_value.overview(search)
    s_overview_smi = scoring.similarites(overview_search, get_value.get_overviews(selected))

    for smi_score in s_overview_smi:
        smi_score = round(smi_score, 3) * 100
        score_list.append(smi_score)

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
        smi_score = sorted_c_overview_smi[lot][1]
        smi_score = round(smi_score,3)*100
        score_list.append(smi_score)
        selected.append(candidates[lot])

    ## 반환은 선택군과, 점수표를 반환
    return selected, score_list

def refine_data(string):
    if type(string) is list:
        string = str(string)

    return string.replace('[',"").replace("]","").replace("\'","")

def print_result(number, movie, lines):
    title = get_value.title(movie)
    temp_line = str(number)+"."+ title
    print(temp_line)

    lines.append(temp_line)
    
    languages = get_value.languages(movie)
    languages = refine_data(languages)
    
    temp_line = "languages : " + languages
    print(temp_line)

    lines.append(temp_line)
    

    genres = get_value.genres_name(movie)
    genres = refine_data(genres)
    temp_line = "genres : " + genres
    print(temp_line)

    lines.append(temp_line)

    series = get_value.series_name(movie)
    series = refine_data(series)
    if series != "":
        temp_line = "series : " + series
        print(temp_line)

        lines.append(temp_line)
        
    companies = get_value.company_name(movie)
    companies = refine_data(companies)

    if companies != "":
        temp_line = "companies : " + companies
        print(temp_line)

        lines.append(temp_line)

    overview = get_value.overview(movie)
    overview = refine_data(overview)

    if overview != "":
        temp_line = "overview : "+ overview
        print(temp_line)

        lines.append(temp_line)

    vote_ave = get_value.vote_ave(movie)
    vote_ave = refine_data(vote_ave)

    if vote_ave != "":
        temp_line = "vote_ave : "+ vote_ave
        print(temp_line)

        lines.append(temp_line)


    temp_line =""
    print(temp_line)
    
    lines.append(temp_line)
   
def make_html(search, selected):
    lines = []

    temp_line = "[search]"
    lines.append(temp_line)
    print(temp_line)

    print_result("S", search, lines)

    temp_line = "[selected]"
    lines.append(temp_line)
    print(temp_line)

    for top in range(len(selected)):
        print_result(top+1, selected[top], lines)

    return lines

rcv_data = file_load(rcv_file_url_L)

data_file = rcv_data[1:]

search = input_title_to_search(rcv_search_string, data_file)

selected, score_list = recommend(search, data_file, 10)

html_lines = make_html(search, selected)

for i in html_lines:
    print(i)