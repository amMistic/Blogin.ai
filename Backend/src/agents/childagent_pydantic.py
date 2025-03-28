from pydantic import BaseModel, Field
from typing import List

# Selection Agent Output 
class PotentialTopics(BaseModel):
    title: str = Field(..., description="Predicted title based on trends")
    source: str = Field(..., description="Sources contributing to the prediction")
    predicted_impact: str = Field(..., description="Expected impact level: High, Medium, Low")
    rationale: str = Field(..., description="Reason for predicting this topic")
    
class SelectionAgentResponse(BaseModel):
    predicted_topics : List[PotentialTopics]