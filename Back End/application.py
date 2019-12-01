from flask import Flask, render_template, request
from flask_cors import CORS
import urllib.request
import urllib.parse
import json

application = Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*"}})

solr_url = 'http://52.14.177.166:8983/solr/gettingstarted/select?q=text%3A{}&rows=20&fl=id,text,poi_name,created_at,user.profile_image_url,lang,poi_name,country,tweet_urls,tweet_date'

@application.route("/")
def home():
    return render_template("index.html")

@application.route('/query', methods = ['GET'])
def query():
    query = request.args.get('q')
    query = urllib.parse.quote(query)
    url = solr_url.format(query)
    try:
        print(url)
        datatest = urllib.request.urlopen(url)
        docstest = json.load(datatest)['response']['docs']
    except:
        print("An exception occurred for Query: " + query)
        docstest = '[]'
    docstest = json.dumps(docstest)
    return docstest

if __name__ == '__main__':
    application.run(host='0.0.0.0')
