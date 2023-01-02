
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

class Resource(BaseModel):
    registered_date : datetime
    post_id: str
    article_title : str
    article_preview : str
    article_original_body : str
    article_domain_url : str
    article_wordcount : int
    article_url : str
    chatgpt_post_content_attemps : Optional[List] = None
