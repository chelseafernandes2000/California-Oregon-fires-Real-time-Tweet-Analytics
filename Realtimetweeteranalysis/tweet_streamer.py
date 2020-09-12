from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time
analyzer = SentimentIntensityAnalyzer()

conn = sqlite3.connect('OregonFiretwitter.db')
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS oregontweetanalysis (id_str TEXT,created_at REAL, tweet TEXT, sentiment REAL,location TEXT)")
    conn.commit()
create_table()

#consumer key, consumer secret, access token, access secret.
ckey=""     #please add your own by creating a developer account on twitter
csecret=""
atoken=""
asecret=""

class listener(StreamListener):

    def on_data(self, data):
        try:
            data = json.loads(data)
         
            if data["retweeted"]:
                return true
            tweet = unidecode(data['text'])
            time_ms = data['created_at']
            id_str=data["id_str"]
            loc=data["user"]
            location=loc["location"]
            vs = analyzer.polarity_scores(tweet)
            if vs['compound']>= 0.05 : 
                sentiment="Positive" 
        
            elif vs['compound'] <= - 0.05 : 
                sentiment="Negative" 
        
            else : 
                sentiment="Neutral" 
            time.sleep(5)
            #print(F"Created at :{time_ms},text: {tweet},sentiment:{sentiment}, id: {id_str}, location:{location}")
            print(time_ms,tweet,sentiment,id,location)
            c.execute("INSERT INTO oregontweetanalysis (id_str, created_at, tweet, sentiment,location) VALUES (?,?,?, ?, ?)",
                  (id_str, time_ms, tweet, sentiment,location))
            conn.commit()
            
        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Oregon","Oregon wildfires","california fires"])
