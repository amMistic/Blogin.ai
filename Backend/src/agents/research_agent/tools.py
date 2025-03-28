from langchain.agents import Tool

from core.api_client import APIClient

# api client 
client = APIClient()
trending_topics_fetching_tool = Tool(
    name = "trending_topics_fetching_tool",
    description = "Fetch trending topics using the format: {'topic': <topic>, 'count': <count>}",
    func=client.run
)