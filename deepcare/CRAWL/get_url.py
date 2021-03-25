from googlesearch import search
import pandas as pd
import time

data = pd.read_csv("/media/thang/New Volume/Rasa-Chatbot/deepcare/CRAWL/CRAWL/spiders/data.csv")
start_urls = []
for query in data['question']:
    time.sleep(5)
    for j in search(query, num=10, stop=10, pause=2):
        start_urls.append(j)

f = open("link.txt", "a")
for link in start_urls:
    f.write(link+"\n")
f.close()