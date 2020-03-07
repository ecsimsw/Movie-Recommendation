import pandas as pd
import csv

meta_file_url_D = "C:/Users/luraw/OneDrive/Desktop/data/test_meta.csv"
meta_file_url_L = "C:/Users/user/Desktop/data/test_meta.csv"

rating_file_url_D = "C:/Users/luraw/OneDrive/Desktop/data/test_ratings.csv"
rating_file_url_L = "C:/Users/user/Desktop/data/test_ratings.csv"

def temp_db_load(meta_url, rating_url):
    meta_file =[]
    rating_file = []

    with open(meta_url, mode='r', encoding='utf8', errors='ignore') as f:
        csv_ = csv.reader(f)
        for i in csv_:
            meta_file.append(i)

    with open(rating_url, mode='r', encoding='utf8', errors='ignore') as f:
        csv_ = csv.reader(f)
        for i in csv_:
            rating_file.append(i)

    return meta_file, rating_file

#meta_file, rating_file = temp_db_load(meta_file_url_L,rating_file_url_L)

#meta_file = pd.read_csv(meta_file_url_D, engine='python')
#meta_file = pd.read_csv(meta_file_url_D, low_memory= False)

#meta_file = meta_file.head(20000)

def similarites(search, candidates):
    from numpy import dot
    from numpy.linalg import norm
    import numpy as np

    from sklearn.feature_extraction.text import TfidfVectorizer

    tfidf = TfidfVectorizer(stop_words='english')

    candidates.insert(0,search)

    data_tfidf = tfidf.fit_transform(candidates)

    similarities =  data_tfidf.toarray()[0] * data_tfidf[1:,].T

    return similarities

def tfidf():
    from numpy import dot
    from numpy.linalg import norm
    import numpy as np

    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf = TfidfVectorizer(stop_words='english')

    search_string = "he is jin hwan kim"
    data_file = ["he is jin", "he is hwan","she is hong", "metrix is fake"]

    # 검색 데이터와 후보군 데이터를 합침
    data_file.insert(0, search_string)

    # tfidf matrix를 만듦
    data_tfidf = tfidf.fit_transform(data_file)

    # 전체 행렬을 곱할 필요가 없으므로 검색 열[0]을 분리하고, 후보군 행렬([1:,])의 transposed와 곱함.
    # 문자-단어 idf * 단어-문자 idf

    similarities =  data_tfidf.toarray()[0] * data_tfidf[1:,].T

    # 큰 순으로 정렬
    similarities = sorted(similarities, reverse=True)
    print(similarities)

