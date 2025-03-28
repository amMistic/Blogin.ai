from dotenv import load_dotenv
from pprint import pprint
import requests
import os

# Loading Environment Variable
load_dotenv()

# Configure logging
from logging_config import app_logger, reddit_logger, google_trend_logger, twitter_trend_logger



# Fetching Trending Topics From Reddict 
class RedditClient:
    def __init__(self):
        self.base_url = "https://www.reddit.com"
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_relevant_subreddits(self, topic : str, count : int = 5):
        """Search for relevant subreddits based on a given topic"""
        reddit_logger.info(f"Searching for subreddits related to: {topic}")
        try:
            response = requests.get(f"{self.base_url}/subreddits/search.json?q={topic}&limit={2 * count}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                subreddits = [sub["data"]["display_name"] for sub in data["data"]["children"]]
                reddit_logger.info(f"Found relevant subreddits: {subreddits}")
                return subreddits
            else:
                reddit_logger.error(f"Failed to fetch subreddits: {response.status_code}")
                return []
        except Exception as e:
            reddit_logger.error(f"Subreddit Search Error: {e}", exc_info=True)
            return []

    def get_reddit_trending(self, topic):
        """Fetch trending discussions from the most relevant subreddit"""
        subreddits = self.get_relevant_subreddits(topic)
        if not subreddits:
            return []

        for subreddit in subreddits:
            reddit_logger.info(f"Fetching trending topics from r/{subreddit}")
            try:
                response = requests.get(f"{self.base_url}/r/{subreddit}/top.json?limit=10", headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    topics = [post["data"]["title"] for post in data["data"]["children"]]
                    reddit_logger.info(f"Trending Topics from r/{subreddit}: {topics}")
                    return topics
                else:
                    reddit_logger.error(f"Failed to fetch Reddit topics from r/{subreddit}: {response.status_code}")
            except Exception as e:
                reddit_logger.error(f"Reddit API Error: {e}", exc_info=True)
        
        return []  # Return empty if no topics found



# Fetching Trending Topics using Google Trends API
class GoogleTrends:
    def __init__(self):
        """
        Initialize the GoogleTrends instance.
        """
        self.base_url = "https://google-news13.p.rapidapi.com/search"
        self.headers = {
            "x-rapidapi-key": os.getenv('X_RAPIDAPI_KEY_GOOGLE_API'),
            "x-rapidapi-host": "google-news13.p.rapidapi.com"
        }
        
    def get_trending_topics(self, topic: str, count : int = 5):
        """
        Fetch trending topics related to a given keyword.

        :param topic: The search keyword.
        :return: List of trending topics or an error message.
        """
        try:
            self.params = {"keyword": f"{topic}", "lr": "en-US"}
            google_trend_logger.info(f"Fetching trending topics for: {topic}")

            response = requests.get(self.base_url, headers=self.headers, params=self.params, timeout=30)
            response.raise_for_status()

            data = response.json()
            max_items = min(2 * count, len(data.get("items", [])))  # Ensure it doesn't exceed available items

            trending_topics = [
                {
                    "title": item["title"],
                    "summary": item["snippet"],
                    "source": item["newsUrl"]
                }
                for item in data.get("items", [])[:max_items]  # Limit to 2 * count
            ]

            google_trend_logger.info(f"Found {len(trending_topics)} trending topics for '{topic}'")
            return trending_topics
            
        except requests.exceptions.Timeout:
            google_trend_logger.error("Request timed out while fetching Google Trends data.")
            return "Error: Request timed out."

        except requests.exceptions.HTTPError as http_err:
            google_trend_logger.error(f"HTTP error occurred: {http_err}")
            return f"Error: HTTP error {response.status_code}"

        except requests.exceptions.RequestException as req_err:
            google_trend_logger.error(f"Request failed: {req_err}")
            return "Error: Failed to fetch data. Please try again later."

        except Exception as e:
            google_trend_logger.error(f"Unexpected error: {str(e)}")
            return "Error: An unexpected error occurred."
        

class TwitterTrends:
    def __init__(self,):
        """
        Initialize the GoogleTrends instance.
        """
        self.base_url = "https://twitter241.p.rapidapi.com/search"
        self.headers = {
            "x-rapidapi-key": os.getenv('X_RAPIDAPI_KEY_TWITTER_API'),
            "x-rapidapi-host": "twitter241.p.rapidapi.com"
        }
        
    def get_trending_topics(self, topic: str, count : int = 5):
        """
        Fetch trending topics related to a given keyword.
        Args : 
            - topic: The search keyword.
            - count : Number of tweets to fetch
        :return: List of trending topics or an error message.
        """
        self.params = { "query" : f'{topic}', "type" : "Latest", "count" : str(2 * count + 2)}
        
        try:
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=self.params,
                timeout=15
            )
            response.raise_for_status()

            data = response.json()
            trending_topics = []

            instructions = data.get('result', {}).get('timeline', {}).get('instructions',[])
            if not instructions:
                twitter_trend_logger.warning("No instructions found in the response.")
                return trending_topics

            entries_list = instructions[0].get('entries', {})
            for i in range(1, len(entries_list)-1):
                try:
                    # Nested access with .get() for safety
                    full_text = (
                        entries_list[i]
                        .get('content', {})
                        .get('itemContent', {})
                        .get('tweet_results', {})
                        .get('result', {})
                        .get('legacy', {})
                        .get('full_text', "No Content Available")
                    )
                    trending_topics.append(f'tweet {i} : {str(full_text)}')
                except Exception as e:
                    twitter_trend_logger.warning(f"Error accessing entry {i}: {e}")

            twitter_trend_logger.info(f"Found {len(trending_topics)} trending topics for '{topic}'")
            return trending_topics

        except requests.exceptions.Timeout:
            twitter_trend_logger.error("Request timed out while fetching Google Trends data.")
            return "Error: Request timed out."

        except requests.exceptions.HTTPError as http_err:
            twitter_trend_logger.error(f"HTTP error occurred: {http_err}")
            return f"Error: HTTP error {response.status_code}"

        except requests.exceptions.RequestException as req_err:
            twitter_trend_logger.error(f"Request failed: {req_err}")
            return "Error: Failed to fetch data. Please try again later."

        except Exception as e:
            twitter_trend_logger.error(f"Unexpected error: {str(e)}")
            return "Error: An unexpected error occurred."

class APIClient:
    def __init__(self):
        self.reddit_trend_client = RedditClient()
        self.twitter_trend_client = TwitterTrends()
        self.google_trend_client = GoogleTrends()

    def run(self, topic: str, count: int = 5):
        """
        Fetches trending topics from Google Trends, Twitter, and Reddit.

        :param topic: The search topic.
        :param count: Number of trending topics to fetch from Twitter.
        :return: Dictionary containing trends from all sources.
        """
        app_logger.info(f"Starting trend fetch for topic: '{topic}' with count: {count}")
        
        response = {
            "google_trends": [],
            "twitter_latest_discussion": [],
            "reddit_latest_discussion": []
        }

        try:
            # Fetch Google Trends
            app_logger.info("Fetching Google Trends...")
            google_trends = self.google_trend_client.get_trending_topics(topic)
            response["google_trends"] = google_trends if google_trends else ["No Google Trends available"]
            app_logger.info(f"Google Trends fetched successfully: {len(google_trends)} items")

        except Exception as e:
            app_logger.error(f"Error fetching Google Trends: {e}")
            response["google_trends"] = [{"error": "Failed to fetch Google Trends"}]

        try:
            # Fetch Twitter Trends
            app_logger.info("Fetching Twitter Discussions...")
            twitter_discussions = self.twitter_trend_client.get_trending_topics(topic, count)
            response["twitter_latest_discussion"] = twitter_discussions if twitter_discussions else ["No Twitter discussions available"]
            app_logger.info(f"Twitter Discussions fetched successfully: {len(twitter_discussions)} items")

        except Exception as e:
            app_logger.error(f"Error fetching Twitter Discussions: {e}")
            response["twitter_latest_discussion"] = [{"error": "Failed to fetch Twitter Discussions"}]

        try:
            # Fetch Reddit Trends
            app_logger.info("Fetching Reddit Discussions...")
            reddit_discussions = self.reddit_trend_client.get_reddit_trending(topic)
            response["reddit_latest_discussion"] = reddit_discussions if reddit_discussions else ["No Reddit discussions available"]
            app_logger.info(f"Reddit Discussions fetched successfully: {len(reddit_discussions)} items")

        except Exception as e:
            app_logger.error(f"Error fetching Reddit Discussions: {e}")
            response["reddit_latest_discussion"] = [{"error": "Failed to fetch Reddit Discussions"}]

        app_logger.info("Trend fetch process completed.")
        return response
        
        
# Example Usage
if __name__ == "__main__":
    topic = 'Artificial Intelligence'
    client = APIClient()
    response = client.run(topic, count=5)
    pprint(response, width=100, indent=4)
    
    