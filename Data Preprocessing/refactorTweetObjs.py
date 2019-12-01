import json
import emoji
import time

loc = "C:/Users/Harshali/AppData/Local/Programs/Python/Python37/TweetReplies"
POIName = '/narendramodi'

data = json.load(open(loc + POIName + '.json', 'r'))

def replaceColorCode(data):
    for attr,val in data.items():
        if type(val) is dict:
            replaceColorCode(val)
        elif 'color' in attr and '#' not in val:
            data[attr] = '#' + val
    
def round_to_hour(dt):
    return time.strftime('%Y-%m-%dT%H:0:0Z', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

with open(loc + POIName + '-refactored.json', 'w') as twFile:
    twFile.write('[\n')
    tcnt = 0
    for tweet in data:
        if tcnt > 0:
            twFile.write(',')
        replaceColorCode(tweet)
        tweet['poi_name'] = tweet['user']['screen_name']
        tweet['poi_id'] = tweet['user']['id']
        tweet['verified'] = tweet['user']['verified']
        tweet['country'] = 'Brazil'
        tweet["replied_to_tweet_id"] = tweet['in_reply_to_status_id_str']
        tweet["replied_to_user_id"] = tweet['in_reply_to_user_id_str']
        if tweet['in_reply_to_user_id'] is not None:
            tweet["reply_text"] = tweet['text']
        else:
            tweet["reply_text"] = ''
        tweet["tweet_text"] = tweet['text']
        tweet["tweet_lang"] = tweet['lang']
        if len(tweet['entities']["hashtags"]) > 0:
            tweet["hashtags"] = []
            for h in tweet['entities']["hashtags"]:
                tweet["hashtags"].append(h['text'])

        if len(tweet['entities']["user_mentions"]) > 0:
            tweet["mentions"] = []
            for m in tweet['entities']["user_mentions"]:
                tweet["mentions"].append(m['screen_name'])

        if len(tweet['entities']["urls"]) > 0:
            tweet["tweet_urls"] = []
            for u in tweet['entities']["urls"]:
                tweet["tweet_urls"].append(u['url'])
                
        tweet["tweet_emoticons" ] = ''.join(c for c in tweet['text'] if c in emoji.UNICODE_EMOJI)
        tweet["tweet_date"] = str(round_to_hour(tweet['created_at']))
        twFile.write(json.dumps(tweet))
        tcnt = tcnt + 1
    twFile.write('\n]')
