import bson
from database.models import LinkedInPost, MediumPost, NewsletterArticle
from typing import List, Union, Type
import mongoengine

def linkedin_get_all_posts_ids() -> List[int]:
    post_ids = LinkedInPost.objects().all()
    post_ids = [post_id.post_id for post_id in post_ids]
    
    return list(post_ids)

def linkedin_get_all_posts() -> List[LinkedInPost]:
    posts = LinkedInPost.objects().all()
    return list(posts)

def get_all_documents(collection : Type[mongoengine.Document]) -> List:
    documents = collection.objects.all()
    return list(documents)

def find_post_by_id_linkedin(post_id : Union[int,str]) -> LinkedInPost:
    post = LinkedInPost.objects(post_id=post_id).first()
    return post



def linkedin_create_post_bulk(contents : List[dict[str,str]]) -> dict[str,str]:

    # get existing posts
    collection_post_ids = linkedin_get_all_posts_ids()
    
    posts = []

    for content in contents:
        if int(content['post_id']) not in collection_post_ids:
            # add post
            post = LinkedInPost()
            post.post_content = content.get('post_content')
            post.post_id = content.get('post_id')
            post.post_link_id = content.get('post_link_id')
            post.post_link = content.get('post_link')
            post.thumbnail_url = content.get('thumbnail_url')
            post.author_tagline = content.get('author_tagline')
            post.author_name = content.get('author_name')
            post.author_url = content.get('author_url')

            posts.append(post) 
        
    if len(posts)>0:
        
        LinkedInPost.objects().insert(posts)
        return {'msg': f'Successfully added {len(posts)}'}

    return {'msg':'No updates to be inserted.'}
  



def newsletter_get_all_article_ids() -> List[str]:
    articles = NewsletterArticle.objects().all()
    article_ids = [article.post_id for article in articles]
    
    return list(article_ids)

def newsletter_get_all_posts() -> List[NewsletterArticle]:
    articles = NewsletterArticle.objects().all()
    return list(articles)



from typing import Dict, Type

def bulk_insert(contents : List[Dict[str,str]], collection : Type[mongoengine.Document], document_type : Type):

    collection_documents_ids = [doc['post_id'] for doc in collection.objects.all()]

    documents = []

    for content in contents:
        if str(content['post_id']) not in  collection_documents_ids:
            document = document_type(**content)
            documents.append(document)

    if len(documents)>0:
        collection.objects.insert(documents)
        return {'msg': f'Successfully added {len(documents)}'}

    return {'msg':'No updates to be inserted.'}


def newsletter_bulk_insert(contents : List[dict[str,str]]) -> dict[str,str]:

    # get existing posts
    collection_post_ids = newsletter_get_all_article_ids()
    
    articles = []

    for content in contents:
        if int(content['post_id']) not in collection_post_ids:
            # add post
            article = NewsletterArticle()
            article.post_id = content.get('post_id')
            article.article_title = content.get('article_title')
            article.article_preview = content.get('article_preview')
            article.article_original_body = content.get('article_original_body')
            article.article_domain_url = content.get('article_domain_url')
            article.article_url = content.get('article_url')
            article.publisher_onboarded = content.get('publisher_onboarded')
            articles.append(article) 
        
    if len(articles)>0:
        
        NewsletterArticle.objects().insert(articles)
        return {'msg': f'Successfully added {len(articles)}'}

    return {'msg':'No updates to be inserted.'}



############ 

def approve_post(post : Union[MediumPost,LinkedInPost,NewsletterArticle]) -> dict:

    if post.post_id is None:
        return {'error':'Post ID not selected'}

    if post.post_source=='linkedin':
        
        post = find_post_by_id_linkedin(int(post.post_id))
        
        LinkedInPost.objects(post_id=post.post_id).update_one(set__is_approved=True)

        new_post = find_post_by_id_linkedin(int(post.post_id))
        
        if post.is_approved!=new_post.is_approved:
            return {'msg': f'Successfully updated post {new_post.post_id}'} 
        
        return {'error':f'Post {new_post.post_id} was already approved.'}


    return {'error':'trying to update non linkedin post'}
