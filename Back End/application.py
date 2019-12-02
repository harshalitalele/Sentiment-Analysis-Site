from flask import Flask, render_template, request
from flask_cors import CORS
import urllib.request
import urllib.parse
import json

application = Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*"}})

solr_ip = 'http://18.223.117.41:8983/solr/IRProject4/'
tweets_url = solr_ip + 'select?q={}&rows=20&fq=-in_reply_to_status_id:{}&fl=id,text,poi_name,created_at,user.profile_image_url,lang,poi_name,country,tweet_urls,tweet_date,user.entities.url.urls.expanded_url'
replies_url = solr_ip + 'select?q={}&rows=20&fl=id,text,poi_name,created_at,lang,poi_name,country'

@application.route("/")
def home():
    return render_template("index.html")

@application.route('/query', methods = ['GET'])
def query():
    query = 'text:' + request.args.get('q')
    query = urllib.parse.quote(query)
    facetq = urllib.parse.quote('[* TO *]')
    url = tweets_url.format(query, facetq)
    try:
        datatest = urllib.request.urlopen(url)
        docstest = json.load(datatest)['response']['docs']
    except:
        print("An exception occurred for Query: " + query)
        docstest = '[]'
    docstest = json.dumps(docstest)
    return docstest

def getTweetIds(query):
    idurl = 'http://18.223.117.41:8983/solr/IRProject4/select?q={}&rows=100&fl=id&fq=-in_reply_to_status_id:{}'
    query = 'text:' + urllib.parse.quote(query)
    facetq = urllib.parse.quote('[* TO *]')
    url = idurl.format(query, facetq)
    
    try:
        datatest = urllib.request.urlopen(url)
        docstest = json.load(datatest)['response']['docs']
    except:
        print("An exception occurred for Query: " + query)
        docstest = '[]'
    return docstest

@application.route('/replies', methods = ['POST'])
def getReplies():
    q = request.get_json().get('query')
    ids = getTweetIds(q)
    print(len(ids))
    query = ''
    count = 0
    for id in ids:
        if count > 0:
            query += ' OR '
        else:
            count += 1
        query += 'in_reply_to_status_id: ' + id['id']
    print(query)
    query = urllib.parse.quote(query)
    url = replies_url.format(query)
    
    try:
        datatest = urllib.request.urlopen(url)
        docstest = json.load(datatest)['response']['docs']
    except:
        print("An exception occurred for the Query")
        docstest = '[]'
    docstest = json.dumps(docstest)
    return docstest

if __name__ == '__main__':
    application.run(host='0.0.0.0')
