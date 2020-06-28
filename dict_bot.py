import tweepy
import time
import os 
import json
# from difflib import get_close_matches

FILE_NAME ='last_seen_id.txt'

#load JSON data
data = json.load(open("dict_data.json"))

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_KEY = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def retrive_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    print('reteving and replying the tweets')
    output=''

    last_seen_id = retrive_last_seen_id(FILE_NAME)

    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    for mention in reversed(mentions):
            print(str(mention.id)+ ' - ' + mention.full_text)
            last_seen_id = mention.id
            store_last_seen_id(last_seen_id, FILE_NAME)
            if '#getmeaning' in mention.full_text.lower():
                word = mention.full_text.lower().replace('#getmeaning', '').replace('@_man_f', '').strip()
                meaning = getMeaning(word)
                print('replying back with results')
                if type(meaning) == list:
                    for item in meaning:
                        output= output + (item +' ; ')
                else:
                    output=meaning
                output= output[:250]
                api.update_status('@' + mention.user.screen_name + ' ' + output, mention.id)
            




def getMeaning(w):
    if w in data:
        return data[w]
    else:
        return "The word doesn't exist. Please double check it."








while True:
    reply_to_tweets()
    time.sleep(30)
