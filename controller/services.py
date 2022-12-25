import bson
from database.models import Author, LinkedInPost, MediumPost
from typing import List


def linkedin_get_all_posts() -> List[int]:
    post_ids = LinkedInPost.objects().all()
    post_ids = [post_id.post_id for post_id in post_ids]
    
    return list(post_ids)

def linkedin_create_post_bulk(contents : List[dict[str,str]]) -> dict[str,str]:

    # get existing posts
    collection_post_ids = linkedin_get_all_posts()
    
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
  
from typing import Union

def find_post_by_id_linkedin(post_id : Union[int,str]) -> LinkedInPost:
    post = LinkedInPost.objects(post_id=post_id).first()
    return post

def find_post_by_id_medium(post_id : Union[int,str]) -> LinkedInPost:
    post = MediumPost.objects(post_id=post_id).first()
    return post


def approve_post(post : Union[MediumPost,LinkedInPost]) -> dict:

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
