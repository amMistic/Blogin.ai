from keyword_extraction_agent import KeywordExtractionAgent
from prompts import prompts

class SuperAgent:
    def __init__(self):
        
        # 1. Agent : Keyword Extraction Agent
        self.keyword_extraction_agent = KeywordExtractionAgent(tools=[], prompt=prompts['KeywordExtractionAgent'])
        
        # 2. Agent : Research Agent 
        self.research_agent = None
        
    def run(self, query : str):
        # workflow 
        # 1. User --> SuperAgent(Keywords Extraction Agent)
        keywords = self.keyword_extraction_agent.run(query)
        
        # 2. SuperAgent(Keywords Extraction Agent) ---> Research Agent
        list_of_topics = self.research_agent.run(keywords)
        
        # pass it to user for selecting one title from the given list of topics
        