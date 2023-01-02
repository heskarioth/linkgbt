from starlite import Starlite, get, State, Response, Router
from typing import List


# from restapp.controllers.controllers import UserController
from restapp.models.models import Resource
from restapp.dependencies import get_db_connection, close_db_connection
from database.models import LinkedInPost, NewsletterArticle


@get("/articles")
def get_all_articles() -> List[Resource]:
    responses = []
    articles = [p.to_mongo().to_dict() for p in NewsletterArticle.objects().all()]#[0]
    for article in articles:
        responses.append(Resource(**article))
    return responses

from typing import Any, Union
from mongoengine import DoesNotExist

@get("/articles/{post_id:str}") 
def get_single_article(post_id : str) -> Union[Resource,Response]:
    print(post_id)
    response = NewsletterArticle.objects(post_id=post_id).first()
    if  response is not None:
        return Resource(**response.to_mongo().to_dict())
    return Response(content={'status_code':'400','msg': f'post not found for {post_id}'})


articles_routes = Router(path='/base',route_handlers=[get_single_article,get_all_articles])


app = Starlite(
    route_handlers=[articles_routes],
    on_startup=[get_db_connection],
    on_shutdown=[close_db_connection],
    initial_state={"count": 100},
    debug=True)

# uvicorn restapp.main:app --reload