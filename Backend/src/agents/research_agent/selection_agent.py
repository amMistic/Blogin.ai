from langchain.schema import SystemMessage, HumanMessage 
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_groq import ChatGroq

from dotenv import load_dotenv
import json

from tools import search_trending_topic_tool, selection_tool
from data_acquisition import DataAcquisition 

# load environmental variable
load_dotenv()

class SelectionAgent:
    def __init__(self, tools : list, trending_topics :str):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
            max_retries=2,
            response_format = "json"
        )
        self.trending_topics = trending_topics
        self.tools = tools
        
    def selection_trending(self, trending_topics : str) -> str:
        system_prompt = f'''
        You are a Research Agent responsible for selecting the best trending HR topic for content creation. You receive trending topics from Twitter, Reddit, and HRDive in JSON format. Your goal is to:
        1. **Analyze** all trending topics.
        2. **Evaluate** based on relevance, engagement, and popularity.
        3. **Select the best topic** for content planning.
        4. **Ensure a structured JSON output** with `title`, `source`, and `url`.
        
        ## Input JSON Format:
        {trending_topics}
        
        ## Selection Criteria:
        1. **Relevance**: Must be directly related to HR, workforce trends, hiring, or business.
        2. **Engagement**: Must have high user engagement (likes, shares, comments).
        3. **Recency**: Must be **trending now** (not old topics).
        4. **Credibility**: Prioritize **HRDive** over social media unless Twitter/Reddit has exceptional engagement.

        ## **Final Output Format:**
        "{
            "selected_topic" : "Topic Name",
            "source" : "Twitter | Reddit | HRDive,"
            "url" : "url"
        }"

        '''
        # get the response from the selection agetn
        response = self.llm.invoke([SystemMessage(content=system_prompt)])
        return response.content
    
    def run(self):
        # create a tool
        selection_agent = initialize_agent(
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Simple reasoning + tool usage
            tools = self.tools, # Assign tool
            llm=self.llm,
            verbose=True  # Enable logging for debugging
        )
        
        response = selection_agent.invoke(self.trending_topics)
        return response
    
if __name__ == '__main__':
    da = DataAcquisition()
    trending_topics = da.run(5)

    tools = [selection_tool]
    sa = SelectionAgent(tools=tools, trending_topics=trending_topics)
    print(json.dumps(sa.run()))
    