from pydantic import BaseModel, Field
from typing import List

# Selection Agent Output 
class PotentialTopics(BaseModel):
    title: str = Field(description="Predicted title based on trends")
    source: str = Field(description="Sources contributing to the prediction")
    predicted_impact: str = Field(description="Expected impact level: High, Medium, Low")
    rationale: str = Field(description="Reason for predicting this topic")
    
class SelectionAgentResponse(BaseModel):
    predicted_topics : List[PotentialTopics]


# Content Planning Agent
class Subheading(BaseModel):
    subheading: str = Field(description="Clear and engaging subheading text to organize content within a section")
    key_keywords: List[str] = Field(
        description="Relevant keywords to incorporate within this subheading's content",
        min_items=3
    )

class Section(BaseModel):
    heading: str = Field(description="Main section heading that clearly identifies the topic area")
    subheadings: List[Subheading] = Field(
        description="List of subheadings that break down the section into digestible parts",
        min_items=3
    )

class Introduction(BaseModel):
    summary: str = Field(description="Engaging overview that introduces the topic and outlines what readers will learn")
    key_keywords: List[str] = Field(
        description="Primary keywords to incorporate in the introduction",
        min_items=3
    )

class Conclusion(BaseModel):
    summary: str = Field(description="Effective closing that summarizes key points and provides a sense of completion")
    key_keywords: List[str] = Field(
        description="Keywords to reinforce in the conclusion for SEO purposes",
        min_items=1
    )

class ContentPlanningAgentResponse(BaseModel):
    title: str = Field(description="SEO-optimized, compelling title that accurately represents the content")
    introduction: Introduction = Field(description="Opening section that hooks readers and sets expectations")
    sections: List[Section] = Field(
        description="Main content sections that comprehensively cover the topic",
        min_items=2
    )
    estimated_word_count: int = Field(
        description="Projected length of the article in words",
        ge=2000
    )
    seo_keywords: List[str] = Field(
        description="Strategic keywords targeting search intent for this topic",
        min_items=3
    )
    conclusion: Conclusion = Field(description="Final section that reinforces key points and provides closure")