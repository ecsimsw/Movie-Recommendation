import csv
import filter
import get_value

file_url_D = "C:/Users/luraw/OneDrive/Desktop/data/test.csv"
file_url_L = "C:/Users/user/Desktop/data/test_meta.csv"

def temp_db_load(url):
    data_file =[]

    with open(url, mode='r', encoding='utf8', errors='ignore') as f:
        csv_ = csv.reader(f)
        for i in csv_:
            data_file.append(i)
        
        return data_file

data_file = temp_db_load(file_url_L)
index = input("search movie index : ")
search = data_file[int(index)]
selected, candidates = filter.stream_filter(search,data_file, 10)

## Test filter works 

print("s",get_value.languages(search),get_value.series(search),get_value.genres(search), get_value.vote_ave(search))

rank = 1
for line in selected:
    print(rank, get_value.languages(line),get_value.series(line),get_value.genres(line), get_value.vote_ave(line))
    rank+=1
