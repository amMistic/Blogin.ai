from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
import json

from super_agent.pydantic_models import KeywordExtraction
from super_agent.prompts import prompts

class KeywordExtractionAgent:
    def __init__(self, tools : list = []):
        load_dotenv()
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
            max_retries=2,
        )
        self.parser = PydanticOutputParser(pydantic_object=KeywordExtraction)
        self.prompt = prompts['KeywordExtractionAgent'].partial(format_instructions=self.parser.get_format_instructions())
        self.tools = tools
        
    def run(self, query : str):
        # define research agent
        agent = create_tool_calling_agent(
            llm = self.llm,
            tools = self.tools,
            prompt = self.prompt 
        )
        
        # excute the research agent 
        agent_executor = AgentExecutor(agent=agent, tools = self.tools, verbose=True)
        response = agent_executor.invoke({
            'query' : f"{query}"
        })
        return response
        

if __name__ == '__main__':
    agent = KeywordExtractionAgent()
    query = '''
    Write a step-by-step 1500-word blog post on "How to Build a Personal Brand from Scratch." Provide a detailed plan with daily or weekly milestones, actionable tasks, and practical tips on content creation, audience engagement, and networking. Include challenges readers might face and how to overcome them. End with motivational advice and potential benefits of building a strong personal brand. Keep the tone practical and encouraging.
    '''
    
    response = agent.run(query)
    # print(f'Response : {response}\n\n')

    keywords = response.get('output')
    
    if "```" in keywords : 
        keywords = keywords.replace('```json','').replace('```','')
    
    keywords = json.loads(keywords)
    print(f'Keywords : {keywords} \n\n  Blog Specification : {keywords.get('blog_specifications')}')
    
    