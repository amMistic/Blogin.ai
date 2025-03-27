from data_acquisition import DataAcquisition
from selection_agent import SelectionAgent
from langchain.agents import Tool

# find the trending HR related topic
da = DataAcquisition()
search_trending_topic_tool = Tool(
    name="Search_HR_Hot_Topics",
    description="Fetch Hot Topics related to Human Resources(HR)",
    func=da.run
)

# select hot topic and pass it into our desired output
sa = SelectionAgent()
selection_tool = Tool(
    name="Selection Tool",
    description="Analyzed the input and select the most trending topic",
    func=sa.selection_tool
)