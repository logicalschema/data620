from csv import reader
import pandas as pd

list_dict = []

col_names = []

# open file in read mode
with open('Bible.csv', 'r', encoding='utf8') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    for i in header:
    	col_names.append(str(i))

    # Iterate over each row in the csv using reader object
    for row in csv_reader:
    	temp = {}
    	count = 0
    	for name in col_names:
    		temp[name] = row[count]
    		count = count + 1

    	list_dict.append(temp)


for item in list_dict:
    url = 'https://raw.githubusercontent.com/logicalschema/data620/main/Week8/data/bible/original/'
    name = item['\ufeffBook']
    name = name.replace(' ', '%20')
    url = url + name + '.txt'
    item['url'] = url


df = pd.DataFrame(list_dict)

df.to_csv('biblebooks_df.csv', index=False)