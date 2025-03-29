from langchain.agents import create_tool_calling_agent 
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import AgentExecutor
from langchain_groq import ChatGroq

from dotenv import load_dotenv
from typing import List, Any
from pprint import pprint
import json

from agents.childagent_pydantic import ContentPlanningAgentResponse
from core.logging_config import outline_logger
from agents.prompts import prompts

# load environmental variable
load_dotenv()

class ContentPlanningAgent:
    def __init__(self, tools : List[Any] = []):
        """
        Initialize the Content Planning Agent with the given tools.
        """
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
            max_retries=2,
        )
        self.tools = tools
        self.parser = PydanticOutputParser(pydantic_object=ContentPlanningAgentResponse)
        self.prompts = prompts['ContentPlanningAgent'].partial(
            format_instructions=self.parser.get_format_instructions()
        )
        
    def run(self, topic : str , blog_specifications : dict):
        """
        Runs the Content Planning Agent on a given topic.
        
        :param topic: The topic for which to generate a content plan.
        :return: A dictionary containing the agent's response.
        """
        try:
            outline_logger.info(f"Starting Content Planning Agent for topic: {topic}")
            
            agent = create_tool_calling_agent(
            llm = self.llm,
            tools = self.tools,
            prompt = self.prompts
            )
        
            agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose = True)
            response = agent_executor.invoke({
                "query": f'{topic}',
                "blog_specifications" : f"{blog_specifications}",
                "format_instructions": self.parser.get_format_instructions(),
            })
        
            outline_logger.info(f"Agent execution completed successfully for topic: {topic}\n")
            return response
        
        except Exception as e:
            outline_logger.error(f"Error in ContentPlanningAgent: {str(e)}", exc_info=True)
            return {"error": str(e)}

        
    
if __name__ == '__main__':
    
    ra_response = '''
    Selected Agent : {"predicted_topics": [
    {
        "title": "The Future of AI Integration: Model Context Protocol (MCP)",
        "source": "Google Trends, Twitter, Reddit",
        "predicted_impact": "High",
        "rationale": "The Model Context Protocol (MCP) is an open standard that enables developers to build secure, two-way connections between their data sources and AI models. With the support of major AI companies like OpenAI and Anthropic, MCP is poised to revolutionize the way AI models interact with external tools and data sources."      
    },
    {
        "title": "Building Secure and Interoperable AI Systems with MCP",
        "source": "Google Trends, Twitter, Reddit",
        "predicted_impact": "Medium",
        "rationale": "As AI systems become increasingly complex, security and interoperability are becoming major concerns. MCP provides a standardized way for AI models to communicate with external tools and data sources, making it an essential component of building secure and interoperable AI systems."
    },
    {
        "title": "MCP: The Key to Unlocking AI Potential",
        "source": "Google Trends, Twitter, Reddit",
        "predicted_impact": "High",
        "rationale": "MCP has the potential to unlock the full potential of AI by enabling AI models to dynamically discover and use any tool, API, or data source. This could lead to significant advancements in areas like natural language processing, computer vision, and decision-making."
    },
    {
        "title": "The Role of MCP in AI-Driven Automation",
        "source": "Google Trends, Twitter, Reddit",
        "predicted_impact": "Medium",
        "rationale": "MCP is playing a crucial role in AI-driven automation by enabling AI models to interact with external tools and data sources. This could lead to increased efficiency and productivity in areas like customer service, data analysis, and process automation."
    },
    {
        "title": "MCP and the Future of AI Tooling",
        "source": "Google Trends, Twitter, Reddit",
        "predicted_impact": "High",
        "rationale": "MCP is set to revolutionize the way AI models interact with external tools and data sources. With its standardized protocol, MCP is poised to become the de facto standard for AI tooling, enabling developers to build more efficient, secure, and interoperable AI systems."
    }
    ]}
    '''
    
    topic = "The Future of AI Integration: Model Context Protocol (MCP)"
    blog_specifications = {
    "target_audience": "Tech enthusiasts, AI developers, and business leaders interested in AI advancements.",
    "tone_of_voice": "Professional, informative, and engaging.",
    "goal": "Educate readers on the importance of MCP (Model Context Protocol) in AI integration and its impact on the future of AI technology.",
    "keywords": ["MCP", "AI Integration", "Future of AI", "Interoperability", "Security Enhancements"],
    "desired_word_count": 4000,
    "call_to_action": "Encourage readers to explore how MCP can enhance their AI systems and consider adopting it for scalable AI solutions.",
    "writing_style": "Conversational yet authoritative, with detailed explanations and practical examples.",
    "content_depth": "Comprehensive, covering MCP from fundamentals to advanced use cases.",
    "seo_requirements": {
        "primary_keyword": "Model Context Protocol",
        "secondary_keywords": ["MCP", "AI Tooling", "Interoperability", "AI Standards"],
        "meta_description": "Explore the transformative impact of the Model Context Protocol (MCP) on AI integration, security, and future advancements.",
        "alt_text_for_images": "Diagram illustrating MCP's role in AI integration"
    },
    "restrictions": [
        "Avoid overly technical jargon—explain complex terms clearly.",
        "No promotional content—focus on educational value."
    ],
    "examples_to_include": [
        "Real-world use cases of MCP in AI models.",
        "Comparisons with other AI integration protocols."
    ]
}

    cpa = ContentPlanningAgent()
    cpa_response = cpa.run(topic, blog_specifications)
    # print(cpa_response)
    
    # get the output
    outline = cpa_response.get('output')
    
    # convert json string into json
    if "```json" in outline:
        outline = outline.replace("```json",'').replace("```",'')
    outline = json.loads(outline)
    
    print('--------------------- THE FINAL OUTLINE ---------------------------')
    print(json.dumps(outline, indent=4))