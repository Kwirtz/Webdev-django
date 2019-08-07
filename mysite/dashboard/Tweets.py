from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time
import re
import os
analyzer = SentimentIntensityAnalyzer()

#consumer key, consumer secret, access token, access secret.
ckey="z8g5hLznKypiCtwuc7gNU6dbI"
csecret="g22jqYQm5YTE5qwTHX8muVZEjn1ab85lwkWWM1xwhLurnDEJeQ"
atoken="2862380889-t0QJi2qmle9g2PqmpH6QZNmXbMrUQMXlYOlASrI"
asecret="Ln4w0XebY01DYKnE8jLeBpPVSt4GJXYlnrCuFNFEzyOjA"

path = os.getcwd()
parent = os.path.dirname(path)
filename = "Twitterdata.db"
savepath = os.path.join(parent,filename)
conn = sqlite3.connect(savepath)
c = conn.cursor()

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL, lang TEXT, trackword TEXT)")
        c.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        c.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        c.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        c.execute("CREATE INDEX fast_lang on sentiment(lang)")
        c.execute("CREATE INDEX fast_trackword on sentiment(trackword)")
        conn.commit()
    except Exception as e:
        print(str(e))

create_table()

to_track = ["MTGA","LeagueOfLegends","Fortnite","ApexLegends","SSBU","dota2","Hearthstone","Overwatch","PUBG"]


class listener(StreamListener):

    def on_data(self, data):
        try:
            data = json.loads(data)
            if 'RT @' not in data['text']:
                if "extended_tweet" in data:
                    tweet = data['extended_tweet']['full_text']
                else:
                    tweet = unidecode(data['text'])
                words = tweet.split()
                words_casefold = [word.casefold() for word in words]
                language = data['lang'] 
                time_ms = data['timestamp_ms']
                vs = analyzer.polarity_scores(tweet)
                sentiment = vs['compound']
                for i in to_track:
                    for j in words_casefold:
                        if re.findall(f".*{i.casefold()}",j) :
                            subject = i
                            print(tweet, time_ms, sentiment, subject)
                            c.execute("INSERT INTO sentiment (unix, tweet, sentiment, lang, trackword) VALUES (?, ?, ?, ?, ?)",
                                (time_ms, tweet, sentiment,language,subject))
                            conn.commit()
                        else :
                            temp = None
        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)


while True:

    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener(), tweet_mode= 'extended')
        twitterStream.filter(languages=["en","fr"], track=to_track)
    except Exception as e:
        print(str(e))
        time.sleep(5)