# https://github.com/mmabrouk/chatgpt-wrapper
from chatgpt_wrapper import ChatGPT
import controller.services as svc 
from database.database import global_init
from database.models import LinkedInPost, NewsletterArticle
from newsletters.parsers import post_size_controller
from typing import List
import html

linkedin_prompt_0 = "Hi can you help me? I've been working on a long post, but I want to rephrase it and make it suitable to share in my professional network in LinkedIn. It should be shorter than the original blog as well as more engaging. Can you help with that?"

linkedin_prompt_1 = """
     Thanks. This is the blog I wanted to make suitable for LinkedIn audiance:\n\n'REPLACE_TEXT_HERE'\n
     Prompt instructions:
     - Be ORIGINAL. You have to enrich the paragraphs with relevant details to make the text more engaging. You can use your internal training set and add relevant text to mine
     - The post should be no more than 200-250 words, use subheadings and bullet points to break up the text.
     - Craft a compelling headline for the post.
     - Feel free to add emojis.
     - Include a call to action in in the post to encourage my readers to take a specific action by asking thought provoking questions and engage with me. 
     - Include hashtags to increase its visibility and help it reach a wider audience.
     - It should be ready to go. Do not include your text or comments. Just the output.
"""
    
linkedin_prompt_2 = """I like it. Do you think there's another way to make it more succint and more relavant to my audiance of entrepreneurs and software engineers?"""



def update_documents_with_chatgpt_posts():
    botgpt = ChatGPT()

    documents : List[NewsletterArticle] = svc.get_all_documents(NewsletterArticle)

    documents = [document for document in documents if document.has_chatgpt_content==False]

    n_responses = [0,450, 650]
    prompts = [linkedin_prompt_0, linkedin_prompt_1,linkedin_prompt_2]
    print('Fetching GPT responses..')
    for document in documents:
        
        botgpt.new_conversation() # create new conversation for each post

        for idx,TEXT_MAN_LEN in enumerate(n_responses):
            # get full text
            full_text : str = html.unescape(str(document.article_original_body))
            
            # select subsample of original text
            full_text_reduced, _ = post_size_controller(full_text,TEXT_MAX_LEN = TEXT_MAN_LEN)
            
            # prompt instruction
            text_input = prompts[idx].replace('REPLACE_TEXT_HERE',full_text_reduced)

            # send request to chat GPT
            chatgpt_response = botgpt.ask(text_input)
            if idx!=0:
                document.chatgpt_post_content_attemps.append(chatgpt_response)
        
        print(f'Created summary for : {document.id}')
        # change status to GPT content flag
        document.has_chatgpt_content=True
        # save
        document.save()



# botgpt = ChatGPT()


# global_init()
# linkedin_posts : List[LinkedInPost] = svc.linkedin_get_all_posts()

# linkedin_posts = [linkedin_post for linkedin_post in linkedin_posts if linkedin_post.has_chatgpt_content==False][:3]



# n_responses = 2
# for linkedin_post in linkedin_posts:
#     chatgpt_response_bucket : List = []
#     linkedin_text : str = html.unescape(str(linkedin_post.post_content))
#     linkedin_prompt = """
#     I would like you to help me rephrease and improve this linkedin post of mine:\n\n'{}'\n
#     In doing so make sure to:
#     - Be ORIGINAL. You have to enrich the paragraphs with relevant details to make the text more engaging. You can use your internal training set and add relevant text to mine
#     - The post should be no more than 250-300 words, use subheadings and bullet points to break up the text.
#     - Craft a compelling headline for the post.
#     - Feel free to add emojis.
#     - Include a call to action in in the post to encourage my readers to take a specific action by asking thought provoking questions and engage with me. 
#     - Include hashtags to increase its visibility and help it reach a wider audience.
#     - The post should be ready to be share, do not include your text.
#                       """.format(linkedin_text)
    
#     post : LinkedInPost = svc.find_post_by_id_linkedin(int(linkedin_post.post_id))    

#     for _ in range(1,n_responses+1):
#         print(f'Post: {post.post_id} | Asking {_} content.')
#         chatgpt_response = botgpt.ask(linkedin_prompt)
#         post.chatgpt_post_content_attemps.append(chatgpt_response)
#         linkedin_prompt = "Please, be be mindful of causal inference. How would you improve this it? Be more original. Try again"

#     post.has_chatgpt_content=True
#     post.save()