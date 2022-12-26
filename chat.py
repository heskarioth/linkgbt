# https://github.com/mmabrouk/chatgpt-wrapper
from chatgpt_wrapper import ChatGPT
import controller.services as svc 
from database.database import global_init
from database.models import LinkedInPost
from typing import List
import html

botgpt = ChatGPT()


global_init()
linkedin_posts : List[LinkedInPost] = svc.linkedin_get_all_posts()

linkedin_posts = [linkedin_post for linkedin_post in linkedin_posts if linkedin_post.has_chatgpt_content==False][:3]



n_responses = 2
for linkedin_post in linkedin_posts:
    chatgpt_response_bucket : List = []
    linkedin_text : str = html.unescape(str(linkedin_post.post_content))
    linkedin_prompt = """
    I would like you to help me rephrease and improve this linkedin post of mine:\n\n'{}'\n
    In doing so make sure to:
    - Be ORIGINAL. You have to enrich the paragraphs with relevant details to make the text more engaging. You can use your internal training set and add relevant text to mine
    - The post should be no more than 250-300 words, use subheadings and bullet points to break up the text.
    - Craft a compelling headline for the post.
    - Feel free to add emojis.
    - Include a call to action in in the post to encourage my readers to take a specific action by asking thought provoking questions and engage with me. 
    - Include hashtags to increase its visibility and help it reach a wider audience.
    - The post should be ready to be share, do not include your text.
                      """.format(linkedin_text)
    
    post : LinkedInPost = svc.find_post_by_id_linkedin(int(linkedin_post.post_id))    

    for _ in range(1,n_responses+1):
        print(f'Post: {post.post_id} | Asking {_} content.')
        chatgpt_response = botgpt.ask(linkedin_prompt)
        post.chatgpt_post_content_attemps.append(chatgpt_response)
        linkedin_prompt = "Please, be be mindful of causal inference. How would you improve this it? Be more original. Try again"

    post.has_chatgpt_content=True
    post.save()