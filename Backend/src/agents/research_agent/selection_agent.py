from langchain.agents import create_tool_calling_agent 
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import AgentExecutor
from langchain_groq import ChatGroq

from dotenv import load_dotenv
import json

from super_agent.keyword_extraction_agent import KeywordExtractionAgent
from agents.research_agent.tools import trending_topics_fetching_tool
from agents.childagent_pydantic import SelectionAgentResponse
from agents.prompts import prompts

# load environmental variable
load_dotenv()

class SelectionAgent:
    def __init__(self, tools : list):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
            max_retries=2,
        )
        self.tools = tools
        self.parser = PydanticOutputParser(pydantic_object=SelectionAgentResponse)
        self.prompts = prompts['SelectionAgent'].partial(format_instructions=self.parser.get_format_instructions())
        
    def run(self, keywords):
        agent = create_tool_calling_agent(
            llm = self.llm,
            tools = self.tools,
            prompt = self.prompts
        )
        
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose = True)
        response = agent_executor.invoke({
            "query": keywords.get("topic", "Default Query"),
            "format_instructions": self.parser.get_format_instructions(),
            # "title": keywords.get("title", "Default Topic"),
        })
        
        return response
    
if __name__ == '__main__':
    # fetch the keywords
    KEA = KeywordExtractionAgent()
    query = '''
    I want a 2000-word beginner-friendly blog on MCP Server with background context, practical examples, and simple explanations.
    '''
    
    response = KEA.run(query)
    keywords = response.get('output')
    if "```" in keywords : 
        keywords = keywords.replace('```json','').replace('```','')
    keywords = json.loads(keywords)
    print(f'Keywords : {keywords} \n\n Blog Specification : {keywords.get('blog_specifications')}')

    # passing the output from Keyword Extraction Agent -- > SelectionAgent 
    tools = [trending_topics_fetching_tool]
    sa = SelectionAgent(tools=tools)
    sa_repsonse = sa.run(keywords)
    
    print(f'Selected Agent : {sa_repsonse.get('output')}')
    