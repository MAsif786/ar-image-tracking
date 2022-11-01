import mysql.connector
from mysql.connector import Error
from mysql.connector import Error
import tweepy
import time
import requests
from tweepy.auth import OAuthHandler
consumer_key = '6g8yTtFKtdzdd5Y8O0CkZk7d0'
consumer_secret = 'FrzeRqhf8b1fRo5MD5xJ6mWZAL25BFFMDrOWsnQrrESIWaq97q'
username_for_last_tweet = 'hmabubakar313'
access_token='930155901666971648-cM8KS94m8UpDgCmYJ0Kl9HYuLBEaqkX'
access_token_secret='P6G4GUXLpTAdDLjKEyQd2rb7fMSRRG7cQhquymI0fjhOz'


def get_last_tweet(screen_name):
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    public_tweets =api.user_timeline(screen_name=screen_name ,count=1, tweet_mode="extended")
    print(public_tweets[0].id)
    return public_tweets[0].id
x=get_last_tweet(username_for_last_tweet)
while True:
    time.sleep(600)
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='user_token',
                                            user='root',
                                            password='admin123')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
          
            cursor.execute("SELECT * FROM user_login")
            records = cursor.fetchall()
            
            print('calling function\n')
            
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            for row in records:                
                auth.set_access_token(row[0], row[1])
                api = tweepy.API(auth)
                api.retweet(x)
        

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


