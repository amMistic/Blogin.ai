from langchain.agents import Tool

from data_acquisition import DataAcquisition
from pytrends.request import TrendReq

# find the trending HR related topic
da = DataAcquisition()
get_latest_tweets_on_topic = Tool(
    name="Search_HR_Hot_Topics",
    description="Fetch Hot Topics related to Human Resources(HR)",
    func=da.run
) 

# find the trending topics from google trends


# Initialize Pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Get Trending Searches
def get_google_trends(topic: str):
    pytrends.build_payload([topic], cat=0, timeframe='now 1-d', geo='', gprop='')
    trends = pytrends.related_queries()[topic]['top']
    return trends[['query', 'value']].to_dict(orient='records') if trends is not None else []

# Example Usage
print(get_google_trends("Artificial Intelligence"))

