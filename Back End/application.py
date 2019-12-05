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

solr_ip = 'http://18.219.110.31:8983/solr/IRProject4/'
tweets_url = solr_ip + 'select?q={}&rows=10{}&fl=id,tweet_text,user.name,user.profile_image_url,tweet_urls,tweet_date,user.entities.url.urls.expanded_url'
replies_url = solr_ip + 'select?q={}&rows=100&fl=id,tweet_text'

@application.route("/")
def home():
    return render_template("index.html")

@application.route('/query', methods = ['POST'])
def query():
    query = 'tweet_text:' + request.args.get('q')
    query = urllib.parse.quote(query)
    filters = request.get_json().get('data')
    resp = {'tweets': [], 'count': 0}
    facetq = ''
    print(filters)
    for f in filters:
        if f == 'includeReplies':
            if filters[f] == False:
                facetq += '&fq=-in_reply_to_status_id:' + urllib.parse.quote('[* TO *]')
        elif filters[f] != '' and filters[f] != None:
            facetq += '&fq=' + f + ':' + urllib.parse.quote(filters[f])
    print(facetq)
    url = tweets_url.format(query, facetq)
    print(url)
    try:
        datatest = json.load(urllib.request.urlopen(url))
        resp['tweets'] = datatest['response']['docs']
        resp['count'] = datatest['response']['numFound']
    except:
        print("An exception occurred for Query: " + query)
    resp = json.dumps(resp)
    return resp

def getTweetIds(query):
    idurl = 'http://18.219.110.31:8983/solr/IRProject4/select?q={}&rows=100&fl=id,tweet_text&fq=-in_reply_to_status_id:{}'
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

@application.route('/queryanalysis', methods = ['POST'])
def analyzeQueryReq():
    q = request.get_json().get('query')
    overall_report = {'tweet': {}, 'replies': {}, 'metadata': {}}
    tweets = getTweetIds(q)
    metadata = fetchQueryMetadata(q)
    overall_report['metadata'] = metadata
    tw_report = getSentimentReport(tweets)
    overall_report['tweet'] = tw_report
    query = ''
    count = 0
    for id in tweets:
        if count > 0:
            query += ' OR '
        else:
            count += 1
        query += 'in_reply_to_status_id: ' + id['id']
        
    query = urllib.parse.quote(query)
    url = replies_url.format(query)
    
    try:
        datatest = urllib.request.urlopen(url)
        docstest = json.load(datatest)['response']['docs']
    except:
        print("An exception occurred for the Query")
        docstest = '[]'

    re_report = getSentimentReport(docstest)
    overall_report['replies'] = re_report
    report = json.dumps(overall_report)
    return report

def fetchQueryMetadata(query):
    faceturl = 'http://18.219.110.31:8983/solr/IRProject4/select?facet.field=country&facet.field=hashtags&facet.field=tweet_date&facet.field=lang&facet.field=retweeted&facet.field=poi_name&facet=on&q={}&rows=1&fl=id'
    query = 'tweet_text:' + urllib.parse.quote(query)
    url = faceturl.format(query)
    try:
        datatest = urllib.request.urlopen(url)
        docstest = json.load(datatest)['facet_counts']['facet_fields']
    except:
        print("An exception occurred for Query: " + query)
        docstest = '[]'
    return docstest

@application.route('/fetchnews', methods = ['GET'])
def fetchNews():
    q = request.args.get('q')

    metadata = fetchQueryMetadata(q)
    
    person = metadata['poi_name'][0]
    lang = metadata['lang'][0]
    country = metadata['country'][0]
    hashtags = metadata['hashtags'][0]
    rel_date = ''.join(metadata['tweet_date'][0].split('T')[0].split('-'))

    url = ('https://api.nytimes.com/svc/search/v2/articlesearch.json?' +
       'q=' + urllib.parse.quote(q) + '&' +
       #'fq=body:' + urllib.parse.quote('("Twitter ' + person + ' ' + hashtags + '")') + '&'
       'begin_date:' + rel_date + '&' +
       'api-key=yITQBXVGR5TlEbggbWcqG2WYhH6s4uUz')
    
    try:
        news = urllib.request.urlopen(url)
        news = json.load(news)
    except:
        print("An exception occurred for the Query")
        docstest = '[]'
    news = json.dumps(news)
    return news

if __name__ == '__main__':
    application.run(host='0.0.0.0')
