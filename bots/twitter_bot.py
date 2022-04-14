import config
import os
import tweepy
import logging
import time 

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()

def authentication() :
    client = tweepy.Client(bearer_token=config.BEARER_TOKEN,
                           consumer_key=config.API_KEY,
                           consumer_secret=config.API_KEY_SECRET,
                           access_token=config.ACCESS_TOKEN,
                           access_token_secret=config.ACCESS_TOKEN_SECRET)
    return client

def get_tweet_id (client,query) :

    logger.info("Getting the list of tweet id...")
    tweet_id=[]
    tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=10) 
    for tweet in tweets.data:
        tweet_id.append(tweet.id)
    return tweet_id

def likes(client,tweet_id) :

    logger.info("Liking recent tweets...")
    for id in tweet_id :
        client.like(id)
        logger.info("Liked tweet Id : %s", id)

def retweet(client,tweet_id) :

    logger.info("Retweeting recent tweets...")
    for id in tweet_id :
        client.retweet(id)
        logger.info("RT'ed tweet id : %s", id)


def follow_back(client) :

    logger.info("Running the follow back method...")
    flag=False
    follower_list=[]
    auth_data=client.get_me()
    auth_id=auth_data.data.id
    logger.info("Getting my current followers list...")

    followers=client.get_users_followers(auth_id)
    for follower in followers.data :
        follower_list.append(str(follower.id))
    
    followings=[]
    logger.info("Getting my  current following list...")

    with open ('followed.txt', "r") as a:
        for line in a:
            if line=='\n' :
                continue
            line=line.strip()
            followings.append(line)

    with open ('followed.txt', "a") as a:
        for  id in follower_list :
            if id not in followings :
                a.write("\n")
                a.write(str(id))
                client.follow(int(id))
                logger.info("Followed the user Id: %s", int(id))
                flag=True

    if flag is False :
        logger.info("No id to follow...")


    
def main() :
    while True :
        logger.info("Starting things...")
        client=authentication()        
        query="#100DaysOfCode"
        tweet_id=get_tweet_id(client,query)
        likes(client,tweet_id)
        retweet(client,tweet_id)
        follow_back(client)
        logger.info("Sleeping for 30 minutes...")
        time.sleep(1800)
        logger.info("Waking up and resuming...")
        print()


if __name__=='__main__' :
    main()

   

    
        
