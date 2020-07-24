import nltk
import credentials  # Import api/access_token keys from credentials.py
import settings  # Import related setting constants from settings.py
from nltk.stem import WordNetLemmatizer
import re
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import tweepy
from nltk.corpus import stopwords
import pickle
import mysql.connector
import joblib
nltk.download('wordnet')
nltk.download('stopwords')
stop = set(stopwords.words('english'))

import time
import pandas as pd
import datetime
t = time.mktime(time.gmtime())
count = 0

model = load_model('model.h5')
tokenizer = joblib.load('tokenizer.sav')

def decode_sentiment(score, include_neutral=True):
        SENTIMENT_THRESHOLDS = (0.4, 0.7)
        if include_neutral:
            label = 0
            if score <= SENTIMENT_THRESHOLDS[0]:
                label = -1
            elif score >= SENTIMENT_THRESHOLDS[1]:
                label = 1

            return label
        else:
            return -1 if score < 0.5 else 1

def predict(text, include_neutral=True):
        SEQUENCE_LENGTH = 300
        x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=SEQUENCE_LENGTH)
        # Predict
        score = model.predict([x_test])[0]
        # Decode sentiment
        label = decode_sentiment(score, include_neutral=include_neutral)
        return label
    
def cle_tex(text):
    sent = re.sub('[^a-zA-Z]', ' ',text)
    sent = sent.lower()
    sent = [ word for word in sent.split() if word not in stop and len(word) > 2 ]
    sent = ' '.join(sent)
    return sent

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        global t
        global count
        '''
        Extract info from tweets
        '''
        try:
            if status.retweeted:
                # Avoid retweeted info, and only original tweets will be received
                return True
            # Extract attributes from each tweet
            id_str = status.id_str
            created_at = status.created_at
            text = self.lemitizor(status.text)  # Pre-processing the text
            clean_Text = cle_tex(text)
            sentiment = predict(text)
            user_created_at = status.user.created_at
            user_location = self.deEmojify(status.user.location)
            user_description = self.deEmojify(status.user.description)
            user_followers_count = status.user.followers_count
            longitude = None
            latitude = None
            if status.coordinates:
                longitude = status.coordinates['coordinates'][0]
                latitude = status.coordinates['coordinates'][1]

            retweet_count = status.retweet_count
            favorite_count = status.favorite_count

            # Store all data in MySQL
            if mydb.is_connected():
                mycursor = mydb.cursor()
                sql = "INSERT INTO {} (id_str, created_at, text, clean_tweet, sentiment) VALUES (%s, %s, %s, %s, %s)".format(settings.TABLE_NAME)
                val = (id_str, created_at, text, clean_Text, sentiment)
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.close()
                print(text)

            if (int(time.mktime(time.gmtime()) - t) >= 60):
                query = "SELECT id_str, created_at, sentiment FROM {}".format("covid19")
                df = pd.read_sql(query, con=mydb)
                df['created_at'] = pd.to_datetime(df['created_at']).apply(lambda x: x + datetime.timedelta(hours=5,minutes=30))
                result = df.groupby([pd.Grouper(key='created_at', freq='60s'), 'sentiment']).count().unstack(fill_value=0).stack().reset_index()
                result = result.rename(columns={"id_str": "Num of '{}' mentions".format('#covid'), "created_at":"Time"})

                Positive = result.tail(4).iloc[0]["Num of '#covid' mentions"]
                Neutral = result.tail(5).iloc[0]["Num of '#covid' mentions"]
                Negative = result.tail(6).iloc[0]["Num of '#covid' mentions"]

                mycursor = mydb.cursor()
                sql = "SELECT id FROM pastdata"
                df = pd.read_sql(sql, con=mydb)
                if df.shape[0] == 20:
                    count = 0
                    query = "DELETE FROM pastdata WHERE id={}".format(int(df.iloc[0]["id"]))
                    mycursor.execute(query)
                    mydb.commit()
                query = "INSERT INTO pastdata (id,time,positive,neutral,negative) VALUES (%s, %s, %s, %s, %s)"
                val = (count,t*1000,int(Positive), int(Neutral), int(Negative))
                mycursor.execute(query, val)
                mydb.commit()
                mycursor.close()
                count+=1
                t = time.mktime(time.gmtime())

        except Exception as e:
            print(e)

    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, stop srcraping data as it exceed to the thresold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False

    def clean_tweet(self, tweet):
        '''
        Use sumple regex statemnents to clean tweet text by removing links and special characters
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def deEmojify(self,text):
        '''
        Strip all non-ASCII characters to remove emoji characters
        '''
        if text:
            return text.encode('ascii', 'ignore').decode('ascii')
        else:
            return None

    def lemitizor(self, text):
        try:
            lemet = WordNetLemmatizer()
            if text:
                text = self.clean_tweet(text)
                text = text.replace('RT','')
                text = self.deEmojify(text)
                tokenized_tweet = text.split()
                lemetized_tweet = []
                for i in tokenized_tweet:
                    lemetized_tweet.append(lemet.lemmatize(str(i))) # lemmitizing
                return ' '.join(lemetized_tweet)
            else:
                return None
        except:
            return None

mydb = mysql.connector.connect(
    host="", # Enter the host name
    user="", # Enter the user
    password="", # Enter the password
    database="", # Enter the database name
    charset ='utf8'
)

if mydb.is_connected():
    '''
    Check if this table exits. If not, then create a new one.
    '''
    mycursor = mydb.cursor()
    mycursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(settings.TABLE_NAME))
    if mycursor.fetchone()[0] != 1:
        mycursor.execute("CREATE TABLE {} ({})".format(settings.TABLE_NAME, settings.TABLE_ATTRIBUTES))
        mydb.commit()
    mycursor.close()

auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

while(1):
    try:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
        myStream.filter(languages=["en"], track = settings.TRACK_WORDS,locations=[68.1766451354, 7.96553477623, 97.4025614766, 35.4940095078])
    except:
        pass
mydb.close()