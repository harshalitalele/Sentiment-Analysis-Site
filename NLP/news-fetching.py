from newsapi import NewsApiClient
import urllib.parse

import requests

topics = 'bulbul cyclone'
date = '2019-11-08'
hashtags = []
person = 'narendra modi'
keywords = ['tweet', 'twitter']

#sample_req = https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=2128fba7ce894df3baa69c9a88318ec8

url = ('https://newsapi.org/v2/everything?' +
       'q=' + urllib.parse.quote(topics + ' ' + person) + '&' +
       'from=' + date + '&' +
       'sortBy=relevancy&' +
       'pageSize=5&' +
       'apiKey=2128fba7ce894df3baa69c9a88318ec8')

print(url)
response = requests.get(url)

res_json = response.json()

for i in res_json['articles']:
    print(i['title'] + '  ---  ' + i['publishedAt'])
