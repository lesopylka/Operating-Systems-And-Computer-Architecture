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
import socket
from datetime import datetime

HOST = "127.0.0.1" 
PORT = 65432  

def log_server(logger):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                logger.handle(data.decode('utf-8'))

                    
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


def logger_process():
    logger = logging.getLogger('app')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    logger.info(data.decode('utf-8'))


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


def process_task(queue):
    start = datetime.now()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
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
            
        s.connect((HOST, PORT))
        
        for k in range(len(threads)):
            s.sendall(results[k].encode('utf-8'))
        process_name = current_process().name
        end = datetime.now()
        s.sendall(f'| Process {process_name} done. |\nStart time: {start}\nEnd time: {end}'.encode('utf-8'))
    
    
if __name__ == '__main__':
    queue = Queue()
    logger = logging.getLogger('app')
    logger.addHandler(QueueHandler(queue))
    logger.setLevel(logging.DEBUG)
    logger_p = Process(target=logger_process, daemon=True)
    logger_p.start()
    logger.info('Main process started.')
    processes = [Process(target=process_task, args=(queue,)) for i in range(2)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    logger.info('Main process done.')
    queue.put(None)
