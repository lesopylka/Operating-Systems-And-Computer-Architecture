import random
from random import randrange
from time import sleep
from threading import current_thread
from multiprocessing import current_process
from threading import Thread
from multiprocessing import Process
from multiprocessing import Queue,Pipe
from logging.handlers import QueueHandler
import logging
import string
from datetime import datetime

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


def logger_process(queue,pipe):
    input_conn, output_conn = pipe
    input_conn.close()
    logger = logging.getLogger('app')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    while True:
        message_proc_name = queue.get()
        if message_proc_name is None:
            break
        logger.handle(message_proc_name)
        message_filter = output_conn.recv()
        print(message_filter)


def thread_task(str,results,index):
    start = datetime.now()
    sleep(random.random())
    strbuff=''
    strspl=str.split()
    strbuff = str.replace(' ', '\n')
    strbuff = '\n' + strbuff
    thread_name = current_thread().name
    process_name = current_process().name
    end = datetime.now()
    results[index] = f'\n!!! Thread {thread_name} in process {process_name} done with result: {strbuff} (started with string {str})\nStart time: {start}\nEnd time: {end}'


def process_task(queue,pipe):
    start = datetime.now()
    results=[None]*3
    threads=[None]*3
    input_conn, output_conn = pipe
    output_conn.close()
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
        input_conn.send(results[k])
    process_name = current_process().name
    end = datetime.now()
    logger.info(f'| Process {process_name} done. |\nStart time: {start}\nEnd time: {end}')
    
if __name__ == '__main__':
    queue = Queue()
    input_conn, output_conn = Pipe()
    logger = logging.getLogger('app')
    logger.addHandler(QueueHandler(queue))
    logger.setLevel(logging.DEBUG)
    logger_p = Process(target=logger_process, args=(queue,(input_conn, output_conn)), daemon=True)
    logger_p.start()
    logger.info('Main process started.')
    processes = [Process(target=process_task, args=(queue,(input_conn, output_conn))) for i in range(5)]
    for process in processes:
        process.start()
    
    for process in processes:
        process.join()
    logger.info('Main process done.')
    queue.put(None)
