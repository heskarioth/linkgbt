import asyncio
import logging
from asyncio import PriorityQueue
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from dataclasses import asdict
import json
from .ds import ArticleItem


# global responses
responses = []
# with open('message.json','r') as f:
#     body_messages = json.load(f)
#     body_messages = [d for d in body_messages if d["publisher_onboarded"] ==True]

async def worker(worker_id : int, queue : PriorityQueue, session : ClientSession):
    while not queue.empty():
        # print(f'Worker {worker_id}')
        work_item : ArticleItem = await queue.get()
        # print(f'Worker {worker_id} : Processing {work_item.article_url}')
        result = await process_page(work_item, session)
        responses.append(ArticleItem(
                                    post_id=work_item.post_id,
                                    article_title=work_item.article_title,
                                    article_preview =work_item.article_preview,
                                    article_domain_url = work_item.article_domain_url,
                                    article_url = work_item.article_url,
                                    publisher_onboarded = work_item.publisher_onboarded,
                                    article_original_body = result,
                                    article_wordcount = work_item.article_wordcount
                                    )
            )
        # print(f'Worker {worker_id} : Finished {work_item.article_url}')
        queue.task_done()

async def process_page(work_item : ArticleItem, session : ClientSession):
    try:
        logging.info('processing..')
        response = await asyncio.wait_for(session.get(work_item.article_url),timeout=4)
        body = await response.text()
        soup : BeautifulSoup = BeautifulSoup(body,'html.parser')
        # links = soup.find_all('a',href=True)
        return body
    except asyncio.exceptions.TimeoutError:
        print(f'Timeout {work_item.article_url}')
    except Exception as e:
        logging.exception(f'Error processing url {work_item.article_url}')

async def main(body_messages):
    url_queue = PriorityQueue()

    request_items = [ArticleItem(   
                                priority=idx,
                                post_id=message['post_id'],
                                article_title=message['article_title'],
                                article_preview =message['article_preview'],
                                article_domain_url = message['article_domain_url'],
                                article_url = message['article_url'],
                                publisher_onboarded = message['publisher_onboarded'],
                                article_wordcount= message['article_wordcount']    
                                ) 
                                for idx,message in enumerate(body_messages)]
    
    for request in request_items:
        url_queue.put_nowait(request)
    
    MAX_WORKERS = 10
    async with ClientSession() as session:
        workers = [asyncio.create_task(worker(i,url_queue,session)) for i in range(MAX_WORKERS)]
        # await url_queue.join()
        # [w.cancel() for w in workers]
        await asyncio.gather(url_queue.join(),*workers)

    
    responses_dicts = [asdict(response) for response in responses]
    with open('responses.json','w') as f:
        json.dump(responses_dicts,f)
    
    return responses_dicts

def run_search_content(body_messages):
    # loop = asyncio.get_event_loop()
    # responses = loop.run_until_complete(main(body_messages))
    # return responses
    with open('responses.json', 'r')  as f:
        responses = json.load(f)
    
    return responses

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(main())
# run_search(body_messages)