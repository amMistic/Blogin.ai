from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from dotenv import load_dotenv
from pprint import pprint
import json

from pydantic_models import KeywordExtraction
from prompts import prompts


class KeywordExtractionAgent:
    def __init__(self, tools : list = [], prompt : ChatPromptTemplate = None):
        load_dotenv()
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
            max_retries=2,
        )
        self.parser = PydanticOutputParser(pydantic_object=KeywordExtraction)
        self.prompt = prompt.partial(format_instructions=self.parser.get_format_instructions())
        self.tools = tools
        self.agent = None
        
    def run(self, query : str):
        # define research agent
        self.agent = create_tool_calling_agent(
            llm = self.llm,
            tools = self.tools,
            prompt = self.prompt 
        )
        
        # excute the research agent 
        agent_executor = AgentExecutor(agent=self.agent, tools = self.tools, verbose=True)
        response = agent_executor.invoke({
            'query' : f"{query}"
        })
        return json.dumps(response)
        

if __name__ == '__main__':
    tools = []
    agent = KeywordExtractionAgent(tools=tools, prompt=prompts['KeywordExtractionAgent'])
    query = 'Create a blog on Machine Learning with round 400words and make sure its begginer friendly, more readability, invoved enough math depends on topic with suitable example for each complex topic'
    response = agent.run(query)
    pprint(f'Response : {response} \n\n Response Type : {type(response)} ')
    
    