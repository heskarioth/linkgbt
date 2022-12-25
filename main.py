from linkedin.linkedin import extract_linkedin_posts
from database.database import global_init
import controller.services as svc
import  database.models as models
# from linkedin.send_requests import send_requests
import json


import mongoengine
print(mongoengine.__version__)

global_init()

extract_linkedin_posts()

with open('output_final.json','r') as f:
    data = json.load(f)



# print(svc.linkedin_create_post_bulk(data))

post = models.LinkedInPost()
post.is_approved = True
post.post_id = 7012071391705387008
# post.post_source='roee'
print(svc.approve_post(post))