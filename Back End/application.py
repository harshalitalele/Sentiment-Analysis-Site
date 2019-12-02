from flask import Flask, render_template, request
from flask_cors import CORS
import urllib.request
import urllib.parse
import json
from textblob import TextBlob
from langdetect import detect
from translate import Translator

application = Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*"}})

solr_ip = 'http://18.223.117.41:8983/solr/IRProject4/'
tweets_url = solr_ip + 'select?q={}&rows=20&fq=-in_reply_to_status_id:{}&fl=id,tweet_text,poi_name,created_at,user.profile_image_url,lang,poi_name,country,tweet_urls,tweet_date,user.entities.url.urls.expanded_url'
replies_url = solr_ip + 'select?q={}&rows=50&fl=id,tweet_text'

@application.route("/")
def home():
    return render_template("index.html")

@application.route('/query', methods = ['GET'])
def query():
    print(request.args.get('q'))
    query = 'tweet_text:' + request.args.get('q')
    query = urllib.parse.quote(query)
    print(query)
    facetq = urllib.parse.quote('[* TO *]')
    url = tweets_url.format(query, facetq)
    print(url)
    try:
        datatest = urllib.request.urlopen(url)
        docstest = json.load(datatest)['response']['docs']
    except:
        print("An exception occurred for Query: " + query)
        docstest = '[]'
    docstest = json.dumps(docstest)
    return docstest

def getTweetIds(query):
    idurl = 'http://18.223.117.41:8983/solr/IRProject4/select?q={}&rows=100&fl=id,tweet_text&fq=-in_reply_to_status_id:{}'
    query = 'tweet_text:' + urllib.parse.quote(query)
    facetq = urllib.parse.quote('[* TO *]')
    url = idurl.format(query, facetq)
    
    try:
        datatest = urllib.request.urlopen(url)
        docstest = json.load(datatest)['response']['docs']
    except:
        print("An exception occurred for Query: " + query)
        docstest = '[]'
    return docstest

def getSentimentReport(data):
    report = {'pos': 0, 'neg': 0, 'neut': 0}
    for jsonobj in data:
        tid=jsonobj['id']
        tweet_data=jsonobj['tweet_text'][0]
        analysis=TextBlob(tweet_data)
        if analysis.sentiment[0]>0:
           report['pos']+=1
        elif analysis.sentiment[0]<0:
            report['neg']+=1
        else:
            report['neut']+=1
    return report

@application.route('/replies', methods = ['POST'])
def getReplies():
    q = request.get_json().get('query')
    tweets = getTweetIds(q)
    #print(data)
##    query = ''
##    count = 0
##    for id in ids:
##        if count > 0:
##            query += ' OR '
##        else:
##            count += 1
##        query += 'in_reply_to_status_id: ' + id['id']
##        
##    query = urllib.parse.quote(query)
##    url = replies_url.format(query)
##    
##    try:
##        datatest = urllib.request.urlopen(url)
##        docstest = json.load(datatest)['response']['docs']
##    except:
##        print("An exception occurred for the Query")
##        docstest = '[]'
##    print(len(docstest))
    report = getSentimentReport(tweets)
    report = json.dumps(report)
    return report

if __name__ == '__main__':
    application.run(host='0.0.0.0')
