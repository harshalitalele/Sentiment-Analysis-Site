from flask import Flask, render_template, request
from flask_cors import CORS
import urllib.request
import urllib.parse
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

solr_url = 'http://3.134.81.216:8983/solr/gettingstarted/select?q=text%3A{}&rows=20&fl=id,text,poi_name'

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/query', methods = ['GET'])
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
    app.run(host='0.0.0.0')
