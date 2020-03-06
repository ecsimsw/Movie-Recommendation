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

def genres(line):
    return find_value_tag(line[data_hash['genres']], 'id', 3, char_last=',')

def series(line):
    return find_value_tag(line[data_hash['series']], 'id', 3, char_last=',')

def languages(line):
    if len(line)-1 < data_hash['spoken_language'] :
        return ''

    return find_value_tag(line[data_hash['spoken_language']], 'iso_639_1', pad_lan=4, data_lan=2)

def company(line):
    return find_value_tag(line[data_hash['production_company']], 'id', pad_lan=3, char_last='}')

def vote_ave(line):
    return line[data_hash['vote_ave']]

def vote_cnt(line):
    return line[data_hash['vote_cnt']]

    vote_cnt = []
    for i in predict_set:
        vote_cnt.append(vote_cnt(i))
    return vote_cnt

## 

def isExist(main_set, compare_set):
    for feature in main_set:
        for c in compare_set:
            if feature==c:
                return True

    return False

def sub_list(pre, post):
    for p in post: 
        pre.remove(p)
    return pre

def same_language(search_line, compare_set):
    # 선택 영화의 언어를 포함하고 있는 영화만을 선별한다.

    search_language = languages(search_line)

    new_compare_set = []
    for line in compare_set:
        compare_language = languages(line)
        if isExist(search_language,compare_language):
            new_compare_set.append(line)

    return new_compare_set

def same_series(search_line, compare_set):
    # 같은 시리즈인지 확인한다.

    search_series = series(search_line)

    if search_series != []:
        same_series_set = []
        for line in compare_set:
            compare_series = series(line)
            if isExist(search_series,compare_series):
                same_series_set.append(line)
        return same_series_set

    else:
        return compare_set

def same_genre_score(search_line, compare_set):
    # 찾고자하는 영화의 장르 리스트와 비교군의 장르 리스트가 몇개나 동일한지 센다.

    search_genre = genres(search_line)

    score_set = []
    for line in compare_set:
        score = 0
        compare_genre = genres(line)
        for sg in search_genre:
            for cg in compare_genre:
                if sg==cg:
                    score += 1
        score_set.append(score)

    return score_set

def sort_by_vote_ave(list2sort):
    return sorted(list2sort, key = lambda x : float(x[data_hash['vote_ave']]), reverse =True)

def sort_by_genre_score(search, candidates):
    gs_list = same_genre_score(search,candidates)

    temp_for_sort = []
    for index, value in enumerate(gs_list):
        temp_for_sort.append(list([index,value]))

    order = sorted(temp_for_sort, key = lambda x : x[1], reverse =True)
    
    sorted_by_genre = []

    for o in order:
        index = o[0]
        sorted_by_genre.append(candidates[index])
    
    return sorted_by_genre

def filt_language(search, candidates, n, selected):
    same_movies = same_language(search, candidates)

    r = len(same_movies)

    if  r <= n:
        # 언어가 일치하는 영화가 찾고자하는 추천 개수보다 적다면

        # 해당 언어가 일치하는 영화는 장르가 동일한 점수에 따라 정렬하여 선택군에 추가한다.
        sorted_same_languages = sort_by_vote_ave(same_movies)

        # 같은 언어 영화끼리는 장르 순으로, 장르 점수까지 동일하다면, 평점으로 순위가 결정된다. 
        sorted_same_languages = sort_by_genre_score(search, sorted_same_languages)
        
        for movie in sorted_same_languages:
            selected.append(movie)

        # 더 뽑아야하는 개수를 줄여주고
        n= n-r
        candidates = sub_list(candidates, same_movies)

        # 나머지는 전체 후보군에서 평점순으로 정렬 선택된다.
        sorted_left_candidates = sort_by_vote_ave(candidates)

        # 나머지 영화안에서 장르 순으로, 장르 점수까지 동일하다면, 평점으로 순위를 결정한다.
        sorted_left_candidates = sort_by_genre_score(search, sorted_left_candidates)

        for movie in sorted_left_candidates[0:n]:
            selected.append(movie)

        # n개를 다 뽑았으므로, 후보군은 선택군으로, 더 찾아야할 영화 개수는 0으로 한다.
        candidates = selected
        n = 0

    else:
        # 동일한 언어의 영화가 n보다 크면, 새로운 후보군은 동일한 언어의 영화들이 된다.
        candidates = same_movies

    return candidates,n

def filt_series(search, candidates, n, selected):
    same_movies = same_series(search, candidates)

    r = len(same_movies)

    if  r <= n:
        # 시리즈가 없거나, 찾고자 하는 개수보다 적으면, 그 목록을 평점 순으로 하여, 선택군에 추가한다.
        sorted_same_series = sort_by_vote_ave(same_movies)

        # 같은 시리즈 중, 유사한 장르의 영화를 먼저 선택하고, 장르 점수가 같은 영화끼리는 평점으로 정렬한다.
        sorted_same_series = sort_by_genre_score(search, sorted_same_series)

        for movie in sorted_same_series:
            selected.append(movie)

        # 더 추출하고자 하는 영화 개수는 이전 n값 - 추가한 데이터 개수이다.
        n= n-r

        # 후보군에서 시리즈가 동일한 집합을 뺀 리스트가 새로운 후보군이 된다.
        candidates = sub_list(candidates, same_movies)

    else:
        # 시리즈가 n개 보다 많다면, 다음 필터는 그 영화들 사이에서 걸러져야할 것이다. 즉 후보군은 시리즈 동일 집단이 된다.
        candidates = same_movies

    return candidates,n

def filt_genre(search, candidates, n, selected):
    # 장르 점수에 따라 후보군을 걸러낸다.

    genre_score = same_genre_score(search, candidates)
    max_score = max(genre_score)
    dif_score=0

    # 높은 점수의 영화들을 후보군에 집어넣고, 기대 점수를 하나씩 낮춰가며 영화를 추가한다.

    while(True):
        exprected_score = max_score - dif_score

        if exprected_score ==0:
            return candidates,n

        r = genre_score.count(exprected_score)

        index_list = []
        top_score_list = []

        # 스코어 집합에서 기대 점수에 해당하는 인덱스를 뽑는다.
        for index, value in enumerate(genre_score):
            if value == exprected_score:
                index_list.append(index)

        # 그 인덱스에 해당하는 영화(기대점의 영화들)의 정보를 따로 리스트에 저장한다.
        for index in index_list:
            top_score_list.append(candidates[index])

        if r <= n :
            # 뽑고자하는 영화 개수보다 적으면, 해당 영화들을 평점으로 정렬하여 선택군에 넣는다.
            sorted_same_genre = sort_by_vote_ave(top_score_list)
            for movie in sorted_same_genre:
                selected.append(movie)
            n = n-r
            dif_score+=1

            if n == 0:
                # 뽑고자하는 영화와 추가한 영화 개수가 일치했으면, 더 동작없이 선택군(=[])과 더 추가해야하는 개수, 0을 반환한다.
                candidates = []
                return candidates,0

        else:
            # 뽑고자하는 영화 개수보다 기대점의 영화가 많다면, 그것을 후보군으로 하고 반환한다.
            candidates = top_score_list
            return candidates, n

def stream_filter(search, data_file, n):
    selected = []

    search_list = []
    search_list.append(search)

    candidates = sub_list(data_file, search_list)

    print("number of data : ", len(candidates))

    ## 동일 언어 영화 선택

    same_languages_movies = same_language(search,candidates)
    candidates,n = filt_language(search, candidates, n, selected)
    same_language_cnt = len(candidates)

    if n == 0:
        print("selecting complete")
        candidates =[]
        return selected,candidates
    else:
        print("same languages : ", same_language_cnt)
        print("left_candidates  : ", same_language_cnt)

    ## 동일 시리즈 영화 선택

    same_series_movies = same_series(search, candidates)
    candidates,n = filt_series(search, candidates, n, selected)

    n_series_cnt = len(candidates)
    same_series_cnt = same_language_cnt - n_series_cnt
    left_lots = n

    if n == 0:
        print("selecting complete")
        candidates = []
        return selected,candidates
    else:
        print("same series : ", same_series_cnt)
        print("left candidates : ", n_series_cnt)

    ## 유사 장르 언어 선택

    candidates, n = filt_genre(search, candidates, n, selected)
    filtered_genre = left_lots - n

    if n == 0:
        print("selecting complete")
        candidates = []
        return selected,candidates
    else:
        print("same genre : ", filtered_genre)
        print("left candidates : ", len(candidates))

    # 선택군과 남은 후보군 반환, 남은 선택 횟수는 n-len(selected)로 확인

    return selected, candidates
