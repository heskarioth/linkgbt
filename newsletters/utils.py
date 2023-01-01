import asyncio
import logging
from asyncio import PriorityQueue
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
import json
from typing import Optional

@dataclass(order=True)
class RequestItem:
    priority : int
    url : str = field(compare=False)
    preview : Optional[str] = None
    domain_url : Optional[str] = None

# global responses
responses = []
with open('message.json','r') as f:
    body_messages = json.load(f)
    body_messages = [d for d in body_messages if d["publisher_onboarded"] ==True]

async def worker(worker_id : int, queue : PriorityQueue, session : ClientSession):
    while not queue.empty():
        print(f'Worker {worker_id}')
        work_item : RequestItem = await queue.get()
        print(f'Worker {worker_id} : Processing {work_item.url}')
        result = await process_page(work_item, queue, session)
        responses.append({'url':work_item.url,'preview':work_item.preview,'domain_url':work_item.domain_url,'body':result})
        print(f'Worker {worker_id} : Finished {work_item.url}')
        queue.task_done()

async def process_page(work_item : RequestItem, queue : PriorityQueue, session : ClientSession):
    try:
        logging.info('processing..')
        response = await asyncio.wait_for(session.get(work_item.url),timeout=3)
        body = await response.text()
        soup : BeautifulSoup = BeautifulSoup(body,'html.parser')
        # links = soup.find_all('a',href=True)
        return body
    except asyncio.exceptions.TimeoutError:
        print(f'Timeout {work_item.url}')
    except Exception as e:
        logging.exception(f'Error processing url {work_item.url}')

async def main():
    url_queue = PriorityQueue()

    request_items = [RequestItem(priority=idx,url=message['url'],preview=message['preview'],domain_url=message['domain_url']) for idx,message in enumerate(body_messages)]
    
    for request in request_items:
        url_queue.put_nowait(request)
    
    max_workers = 10
    async with ClientSession() as session:
        workers = [asyncio.create_task(worker(i,url_queue,session)) for i in range(max_workers)]
        # await url_queue.join()
        # [w.cancel() for w in workers]
        await asyncio.gather(url_queue.join(),*workers)
    with open('responses.json','w') as f:
        json.dump(responses,f)

def run_search():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(main())
run_search()