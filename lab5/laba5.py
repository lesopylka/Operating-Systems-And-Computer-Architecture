import random
from random import randrange
from time import sleep
from threading import current_thread
from multiprocessing import current_process
from threading import Thread
from multiprocessing import Process
from multiprocessing import Queue
from logging.handlers import QueueHandler
import logging
import string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def logger_process(queue):
    logger = logging.getLogger('app')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    while True:
        message = queue.get()
        if message is None:
            break
        logger.handle(message)

def thread_task(str,results,index):
    sleep(random.random())
    strbuff=''
    strspl=str.split()
    
    strbuff = str.replace(' ', '\n')
    strbuff = '\n' + strbuff
    thread_name = current_thread().name
    process_name = current_process().name
    results[index] = f'\n!!! Thread {thread_name} in process {process_name} done with result: {strbuff} (started with string {str})'

def process_task(queue):
    results=[None]*3
    threads=[None]*3
    logger = logging.getLogger('app')
    logger.addHandler(QueueHandler(queue))
    logger.setLevel(logging.DEBUG)
    
    for n in range(len(threads)):
        stringa=randomword(randrange(1, 5))+' '+randomword(randrange(1, 5))+' '+randomword(randrange(1, 5))+' '+randomword(randrange(1, 5))
        threads[n] = Thread(target=thread_task, args=([stringa,results,n])) 
        threads[n].start()
    for n in range(len(threads)):
        threads[n].join()
    for k in range(len(threads)):
        logger.info(results[k])
    process_name = current_process().name
    logger.info(f'| Process {process_name} done. |')
    
if __name__ == '__main__':
    queue = Queue()
    logger = logging.getLogger('app')
    logger.addHandler(QueueHandler(queue))
    logger.setLevel(logging.DEBUG)
    logger_p = Process(target=logger_process, args=(queue,), daemon=True)
    logger_p.start()
    logger.info('Main process started.')
    processes = [Process(target=process_task, args=(queue,)) for i in range(5)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    logger.info('Main process done.')
    queue.put(None)
