"""
0: adult
1: siries
2: buget
3: genre
4: homepage
5: id
6: imdb_id
7: original lan
8. original title
9. overview
10. popularity
11. poster
12. production company
13. production lan
14. release
16. revenue
17. runtime
18. spoken lan
19. status
20. tag
21. title
22. video
23. vote_ave
24. vote_cnt
"""

data_hash ={
    'adult' :0,
    'series' : 1,
    'budget' : 2,
    'genres' :3,
    'homepage' :4,
    'id':5,
    'imdb_id':6,
    'original_language':7,
    'original_titile' :8,
    'overview' :9,
    'popularity':10,
    'poster':11,
    'production_company':12,
    'production_country':13,
    'release':14,
    'revenue':15,
    'runtime':16,
    'spoken_language':17,
    'status':18,
    'tagline':19,
    'title':20,
    'video':21,
    'vote_ave':22,
    'vote_cnt':23 }

import csv
data_file =[]

with open("C:/Users/user/Desktop/data/test.csv", mode='r', encoding='utf8', errors='ignore') as f:
    csv= csv.reader(f)    
    for i in csv:
        data_file.append(i)
        #print(i[3].split('}, {'))

def print_list(list_):
    for line in list_:
        print(line)

def find_value_tag(string, char_tag, pad_lan, char_last= None, data_lan =None):
    value = []

    while(True):
        tag_index = string.find(char_tag)

        if tag_index==-1:
            return value

        if data_lan != None:
            start_index = tag_index+pad_lan+len(char_tag)
            last_index = start_index+data_lan
        
        else:
            start_index = tag_index+pad_lan+len(char_tag)
            last_index = string.find(char_last)

        result_value = string[start_index:last_index]
        value.append(result_value)
        
        next_data_index = string.find(", {")

        if next_data_index == -1:
            break
        string = string[next_data_index+1:]

    return value

def get_genres_by_line(line):
    return find_value_tag(line[data_hash['genres']], 'id', 3, char_last=',')

def get_series_by_line(line):
    return find_value_tag(line[data_hash['series']], 'id', 3, char_last=',')

def get_languages_by_line(line):
    return find_value_tag(line[data_hash['spoken_language']], 'iso_639_1', pad_lan=4, data_lan=2)

def get_company_by_line(line):
    return find_value_tag(line[data_hash['production_company']], 'id', pad_lan=3, char_last='}')

def get_vote_ave_by_line(line):
    return line[data_hash['vote_ave']]

def get_vote_cnt_by_line(line):
    return line[data_hash['vote_cnt']]

def get_genres_by_set(predict_set):
    genre_list = []
    for i in predict_set:
        genre_list.append(get_genres_by_line(i))
    return genre_list

def get_series_by_set(predict_set):
    series_list = []
    for i in predict_set:
        series_list.append(get_series_by_line(i))
    return series_list

def get_languages_by_set(predict_set):
    series_list = []
    for i in predict_set:
        series_list.append(get_languages_by_line(i))
    return series_list

def get_company_by_set(predict_set):
    company_list = []
    for i in predict_set:
        company_list.append(get_company_by_line(i))
    return company_list

def get_vote_ave_by_set(predict_set):
    vote_ave = []
    for i in predict_set:
        vote_ave.append(get_vote_ave_by_line(i))
    return vote_ave

def get_vote_cnt_by_set(predict_set):
    vote_cnt = []
    for i in predict_set:
        vote_cnt.append(get_vote_cnt_by_line(i))
    return vote_cnt

def isExist(main_set, compare_set):
    for feature in main_set:
        for c in compare_set:
            if feature==c:
                return True
    
    return False

def filter_language(search_line, compare_set):
    search_language = get_languages_by_line(search_line)

    new_compare_set = [] 
    for line in compare_set:
        compare_language = get_languages_by_line(line)
        if isExist(search_language,compare_language):
            new_compare_set.append(line)
    
    return new_compare_set

def filter_series(search_line, compare_set):
    search_series = get_series_by_line(search_line)

    if search_series != []:   
        new_compare_set = [] 
        for line in compare_set:
            compare_series = get_series_by_line(line)
            if isExist(search_series,compare_series):
                new_compare_set.append(line)
        return new_compare_set
    
    else:
        return compare_set    

def score_set_genre(search_line, compare_set):
    search_genre = get_genres_by_line(search_line)

    score_set = []
    for line in compare_set:
        score = 0
        compare_genre = get_genres_by_line(line)
        for sg in search_genre:
            for cg in compare_genre:
                if sg==cg:
                    score += 1
        score_set.append(score)

    return score_set

index = input("search movie index : ")

search_line = data_file[int(index)]

#filtered = filter_language(search_line, data_file)

#filtered = filter_series(search_line, data_file)

score_set = score_set_genre(search_line, data_file)

print_list(score_set)


