from hrdive_scrapper import HVDiveScrapper
from pytrends.request import TrendReq
from dotenv import load_dotenv
import tweepy
import logging
import json
import praw
import time
import os

load_dotenv()  # Load API keys from .env file

class DataAcquisition:
    def __init__(self):
        """Initialize API clients with credentials from environment variables."""

        self.twitter_api_key = os.getenv("BEARER_TOKEN")
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
        self.pytrends = TrendReq()

        # Initialize Tweepy Client if API key is provided
        if self.twitter_api_key:
            self.client = tweepy.Client(bearer_token=self.twitter_api_key)
        else:
            self.client = None
        

    def reddit_hr_trends(self, subreddit_name="humanresources", limit=5):
        logging.info('Fetching Most Recent Reddit Post...')
        """Fetch top trending HR discussions from Reddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            trending_posts = []
            for post in subreddit.top(limit=limit):  # You can use .top() or .new() as well
                trending_posts.append({
                    "title": post.title,
                    "url": post.url,
                    "score": post.score,
                    "comments": post.num_comments
                })
            logging.info('Subreddit related to Human Resources Fetched Sucessfully!')
        except Exception as e:
            logging.error(f'Error: {e}')
            
        return trending_posts

    def twitter_hr_trends(self):
        """Fetches trending HR-related tweets from Twitter API"""
        if self.client:
            logging.info('Fetching Most Recents Tweets on Human Resources')
            query = "Human Resources -is:retweet lang:en"
            try:
                tweets = self.client.search_recent_tweets(query=query, max_results=10)
                logging.info('Twitter Post Fetched Sucessfully!')
                return [tweet.text for tweet in tweets.data] if tweets.data else "No tweets found."
            except tweepy.TweepyException as e:
                return f"Error fetching tweets: {str(e)}"
        else:
            logging.error('Unable to fetch the tweets. Check for API KEY! Try again later :)')
            raise ValueError("Twitter API key is missing.")
        
    def hrdive_topics(self, max_latest : int = 5):
        scrapper = HVDiveScrapper()
        topics = scrapper.run(max=max_latest)
        return topics
    
    def run(self):
        logging.info('Starts Fetching Trending Topics...')
        tweets = self.twitter_hr_trends()
        reddits = self.reddit_hr_trends()
        topics = self.hrdive_topics()
        final_response = {
            'twitter_hr_trending': tweets,
            'reddit_hr_trending' : reddits,
            'hrdive_trending' : topics
        }
        return json.dumps(final_response, indent=4)

if __name__ == '__main__':
    start_time = time.time()
    da = DataAcquisition()
    response = da.run()
    end_time = time.time()
    
    print(response)
    print(f'Total Time Taken : {float(end_time - start_time)}')
