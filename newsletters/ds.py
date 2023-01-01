from dataclasses import dataclass, field
from typing import Optional

@dataclass(order=True)
class ArticleItem:
    post_id : str
    article_url : str
    article_title : str = field(compare=False)
    article_preview : Optional[str] = None
    article_domain_url : Optional[str] = None
    publisher_onboarded : Optional[bool] = None
    priority : Optional[int] = None
    article_original_body : Optional[str] = None
    wordcount : Optional[int] = None