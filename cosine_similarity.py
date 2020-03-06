import pandas as pd 
import csv 

meta_file_url_D = "C:/Users/luraw/OneDrive/Desktop/data/test.csv"
meta_file_url_L = "C:/Users/user/Desktop/data/test_meta.csv"

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

meta_file = pd.read_csv(meta_file_url_L, low_memory= False)

meta_file = meta_file.head(20000)

"""
meta_file['overview'] = meta_file['overview'].fillna('')
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf.fit_transform(meta_file['overview'])
"""
"""
print(tfidf_matrix)

from sklearn.metrics.pairwise import linear_kernel
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(meta_file.index, index=meta_file['title']).drop_duplicates()

def get_recommendations(title, cosine_sim=cosine_sim):
    # 선택한 영화의 타이틀로부터 해당되는 인덱스를 받아옵니다. 이제 선택한 영화를 가지고 연산할 수 있습니다.
    idx = indices[title]

    # 모든 영화에 대해서 해당 영화와의 유사도를 구합니다.
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 유사도에 따라 영화들을 정렬합니다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 가장 유사한 10개의 영화를 받아옵니다.
    sim_scores = sim_scores[1:11]

    # 가장 유사한 10개의 영화의 인덱스를 받아옵니다.
    movie_indices = [i[0] for i in sim_scores]

    # 가장 유사한 10개의 영화의 제목을 리턴합니다.
    return meta_file['title'].iloc[movie_indices]


#print(get_recommendations('The Dark Knight Rises'))

"""

from numpy import dot
from numpy.linalg import norm
import numpy as np

def cos_sim(A, B):
       # dot : dot product 
       # norm : normalize
       return dot(A, B)/(norm(A)*norm(B))

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english')

meta_file = ["he is jin, sorry it's fake", "he is hwan it's no fake","she is hong", "metrix is hey juyde ! jhi"]

tfidf_matrix = tfidf.fit_transform(meta_file)
print(tfidf.get_feature_names())
print(tfidf_matrix)