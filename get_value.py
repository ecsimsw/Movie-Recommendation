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

def overview(line):
    if len(line)-1 < data_hash['overview'] :
        return ''

    return line[data_hash['overview']]

def title(line):
    if len(line)-1 < data_hash['title'] :
        return ''

    return line[data_hash['title']]

def get_overviews(set_movie):
    overviews = []
    for movie in set_movie:
        overviews.append(overview(movie))

    return overviews

def get_titles(set_movie):
    titles = []
    for movie in set_movie:
        titles.append(title(movie))

    return titles