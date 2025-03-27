from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from dotenv import load_dotenv
from pprint import pprint

from pydantic_models import KeywordExtraction
from prompts import get_prompts


class KeywordExtractionAgent:
    def __init__(self, tools : list = [], trending_topics : str = None, prompt : ChatPromptTemplate = None):
        load_dotenv()
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
            max_retries=2,
        )
        self.parser = PydanticOutputParser(pydantic_object=KeywordExtraction)
        self.prompt = prompt.partial(format_instructions=self.parser.get_format_instructions())
        self.trending_topics = trending_topics
        self.tools = tools
        self.agent = None
        
    def run(self):
        # define research agent
        self.agent = create_tool_calling_agent(
            llm = self.llm,
            tools = self.tools,
            prompt = self.prompt 
        )
        
        # excute the research agent 
        agent_executor = AgentExecutor(agent=self.agent, tools = self.tools, verbose=True)
        response = agent_executor.invoke({
            'query' : f"{input('Hello! How can i help you?\n')}"
        })
        pprint(f'Response : {response.get('output')}')
        

if __name__ == '__main__':
    tools = []
    prompt = get_prompts('KeywordExtractionAgent')
    agent = KeywordExtractionAgent(tools=tools, prompt=prompt)
    agent.run()
    