from langchain.prompts import ChatPromptTemplate
prompts = {
    'KeywordExtractionAgent' : ChatPromptTemplate.from_messages(
        [
            (
                "system",
                '''
                You are a Keywords Extraction Agent designed to identify and 
                extract essential keywords from user-provided text or prompts 
                related to blog generation.Your goal is to identify the main topic, 
                subtopics, constraints, and any specific requirements mentioned in the prompt.
                
                If the prompt is about the blog generation:
                    Wrap the output in this format and provide no other text \n {format_instructions}
                else:
                    Response "you're unable to serve his/her agent" in various style respectfully each time.
                '''
            ),
            ('placeholder', '{chat_history}'),
            ('human' , '{query}'),
            ('placeholder', '{agent_scratchpad}')
        ]
    ),
}
