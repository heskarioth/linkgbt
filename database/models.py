
import mongoengine
import datetime

class Author(mongoengine.EmbeddedDocument):

    # registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    author_tagline = mongoengine.StringField(required=True)
    author_name = mongoengine.StringField(required=True)
    author_url = mongoengine.StringField(required=True)
    post_source=mongoengine.StringField(default='author')

class LinkedInPost(mongoengine.Document):
    
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    post_id = mongoengine.IntField(required=True)
    post_link_id = mongoengine.StringField()
    post_content = mongoengine.StringField(required=True)
    post_link = mongoengine.StringField(required=True)
    thumbnail_url = mongoengine.StringField()
    post_source= mongoengine.StringField(default='linkedin')
    # author = mongoengine.EmbeddedDocumentListField(Author)
    author_tagline = mongoengine.StringField(required=True)
    author_name = mongoengine.StringField(required=True)
    author_url = mongoengine.StringField(required=True)
    
    # chatGBT
    has_chatgpt_content = mongoengine.BooleanField(default=False)
    chatgpt_post_content = mongoengine.StringField(default="")
    chatgpt_post_content_attemps = mongoengine.ListField(defeault=[])
    chatgpt_thumbnail_prompt = mongoengine.StringField(default="")

    # post managements fields
    is_approved = mongoengine.BooleanField(default=False)
    is_thumbnail_required = mongoengine.BooleanField(default=False)

    # we will have to get back to this, we don't want it to post them all on the same day.
    post_planned_date = mongoengine.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=30))

    meta = {
        'db_alias': 'core',
        'collection': 'linkedinposts'
    }



class MediumPost(mongoengine.Document):
    
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    post_id = mongoengine.IntField(required=True)
    post_link_id = mongoengine.StringField()
    post_content = mongoengine.StringField(required=True)
    post_link = mongoengine.StringField(required=True)
    thumbnail_url = mongoengine.StringField()
    post_source= mongoengine.StringField(default='linkedin')
    # author = mongoengine.EmbeddedDocumentListField(Author)
    author_tagline = mongoengine.StringField(required=True)
    author_name = mongoengine.StringField(required=True)
    author_url = mongoengine.StringField(required=True)
    
    # chatGBT 
    chatgbt_post_content = mongoengine.StringField(default="")
    chatgbt_post_content_attemps = mongoengine.ListField(defeault=[])
    chatgbpt_thumbnail_prompt = mongoengine.StringField(default="")

    # post managements fields
    is_approved = mongoengine.BooleanField(default=False)
    is_thumbnail_required = mongoengine.BooleanField(default=False)

    # we will have to get back to this, we don't want it to post them all on the same day.
    post_planned_date = mongoengine.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=30))

    meta = {
        'db_alias': 'core',
        'collection': 'mediumposts'
    }