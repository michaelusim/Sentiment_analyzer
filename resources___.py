import json
from tweepy import streaming
from tweepy import OAuthHandler as Auth_handle
from tweepy import Stream
import sqlite3
from textblob import TextBlob


# connect to our database
conn = sqlite3.connect("twitter_lite.db")
c = conn.cursor()


def create_table():
 
    '''Creates sqllite3 table
    returns sqllite table '''

    
    c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
    conn.commit()
    return create_table()

# defining relevant twitter api keys


consumer_key = "ZOAkAzzg0bp6tuH2OHaxiSSyL"
consumer_secret_key = "i3ITkUKztt4IEjMlEBVqubudMESLhmdA6aKzd5NvyeB6um13g6"
access_token = "3295068475-0ccNF8544ZOeDkZue2znQRQlu2D96VLSQoXZ9fe"
access_secret_token = "c83Amz5coWb3hAoTJnFrvsepkcULDqke8DNsrzY8YoKcR"

issue = streaming.StreamListener


class Listener(issue):
    '''This class will create a stream object and save it to database'''
    def on_data(self, data):
            try:
                data = json.loads(data)  #serialize relevant data from listener
                tweet = (data["text"])   # get data from column "text" and "timestamp_ms"  and define
                time_ms = data['timestamp_ms']
                analysis = TextBlob(tweet)
                sentiment = analysis.sentiment.polarity
                print(time_ms, tweet, sentiment)
                c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",(time_ms, tweet, sentiment)) # save printed to database
                conn.commit()
            except KeyError as e:
                print(str(e))
            return True

    def on_error(self, status):      #error message handling
            print(status)
            return True


auth = Auth_handle(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_secret_token)

twitterStream = Stream(auth, Listener())
twitterStream.filter(track=["Donald Trump"])







