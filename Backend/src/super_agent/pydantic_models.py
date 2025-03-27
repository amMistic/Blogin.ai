from pydantic import BaseModel
from typing import Literal, List
    
# Selection Key - Keywords Extraction
class KeywordExtraction(BaseModel):
    topic : str
    word_counts : int = 2000
    blog_specifications : List[str]
    role : Literal["User"] = "User"
    