import csv
from pprint import pprint

with open('./wait_time_data_20221105.csv', encoding='utf8', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)


dic = {0: '美女と野獣', 1: 'アトラクション2'}