from flask import Flask,redirect,session
import tweepy
from flask import request
from flask import render_template
# from flask_mysqldb import MySQL

from constants import *


app = Flask(__name__, static_folder="templates/assets")
app.secret_key = "3242342342"
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'admin123'
# app.config['MYSQL_DB'] = 'user_token'
# mysql = MySQL(app)


# @app.route('/auth')
@app.route('/')
def auth():
    try:
        print("Call")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
        
        print("Call", dir(auth))
        url = auth.get_authorization_url()
        print("URL: ",url)
        session['request_token'] = auth.request_token
    except Exception as e:
        return render_template('index.html')

    return redirect(url)
    

@app.route('/callback')
def twitter_callback():
    request_token = session['request_token']
    print(request_token)
    del session['request_token']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    print(verifier)
    auth.get_access_token(verifier)
    session['token'] = (auth.access_token, auth.access_token_secret)
    print(session['token'])
    return redirect('/app')

@app.route('/latest_tweet')
def latest_tweet():
    screen_name = request.args.get('username')
    last_tweet = get_last_tweet(screen_name)
    return render_template('tweet_card1.html', tweet=last_tweet, screen_name=screen_name)

@app.route('/app')
def request_twitter():
    try:
        
        token, token_secret = session['token']
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
        
        auth.set_access_token(token, token_secret)
        api = tweepy.API(auth)
        # api.retweet(get_last_tweet_id(username_for_last_tweet)) 
        tweet = get_last_tweet_id(username_for_last_tweet)
        print(tweet)

        return render_template('index.html')
    except Exception as e:
        print(e)
        return render_template('rt.html')


def get_last_tweet(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    if screen_name is None:
        tweets =api.user_timeline(count=1, tweet_mode="extended")
    else:
        tweets =api.user_timeline(screen_name=screen_name, count=1, tweet_mode="extended")
    
    tweet = tweets[0].__dict__
    if len(tweets[0].entities.get('media',[])) > 0:
        tweet["media_url"] = tweets[0].entities.get('media',[])[0].get('media_url')

    return tweet

def get_last_tweet_id(screen_name):
    last_tweet = get_last_tweet(screen_name)
    return last_tweet[0].id



    

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=30006, debug=True, ssl_context='adhoc')