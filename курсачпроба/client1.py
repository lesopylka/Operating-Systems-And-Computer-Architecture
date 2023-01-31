import socket
from threading import current_thread
from multiprocessing import current_process
from threading import Thread
from multiprocessing import Queue
import socket
import random
import time
import logging
from multiprocessing import Process
from multiprocessing import Pipe
import string

HOST = "127.0.0.1" 
PORT_1 = 65430 
PORT_2 = 65429

def client(port,number):
    queue_s = Queue()
    msg = b''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, port))
        item=f'Client {number} started'
        b=bytes(item, encoding='utf-8')
        s.sendall(b)
        processes = [Process(target=process_task_client, args=(queue_s,)) for i in range(number+1)]
        for process in processes:
            process.start()
        for process in processes:
            process.join()
        while queue_s.empty() != True:
            item = queue_s.get()
            b=bytes(item, encoding='utf-8')
            msg = msg + b'|' + b
        item=f'Client {number} done.'
        b=bytes(item, encoding='utf-8')
        msg = msg + b'|' + b
        s.sendall(msg)

def randomword(length):
   letters = string.ascii_lowercase + string.digits
   return ''.join(random.choice(letters) for i in range(length))

def process_task_client(queue_s):
    conn1, conn2 = Pipe(duplex=True)
    conn3, conn4 = Pipe()
    conn5, conn6 = Pipe()
    first_string = randomword(5)+' '+randomword(5)+' '+randomword(5)+' '+randomword(5)+' '
    thread1=Thread(target=thread_task_client, args=([first_string,queue_s,0,conn1,1]))
    thread2=Thread(target=thread_task_client, args=(['',queue_s,conn2,conn3,2])) 
    thread3=Thread(target=thread_task_client, args=(['',queue_s,conn4,conn5,1]))
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    item=conn6.recv()
    queue_s.put(f'Finally {item}')
    process_name = current_process().name
    queue_s.put(f'Process {process_name} done.')

def thread_task_client(str,queue_s,input,output,main_flag):
    time.sleep(random.random())
    if input != 0:
        str = input.recv()
    str_copy = str
    if main_flag == 1:
        flag = 0
        i = 0
        brackets = 0
        while (i != len(str)):
            if (47 < ord(str[i]) < 58) and flag == 0:
                str_copy = str_copy[:i + brackets] + '(' + str_copy[i + brackets:] 
                brackets += 1
                flag = 1
            if (ord(str[i]) < 48 or ord(str[i]) > 57) and  flag == 1:
                str_copy = str_copy[:i + brackets] + ')' + str_copy[i + brackets:] 
                brackets += 1
                flag = 0
            i += 1
            if i == len(str) and flag == 1:
                str_copy = str_copy[:i + brackets] + ')' + str_copy[i + brackets:] 
                brackets += 1
                flag = 0
    else:
        strcopy=''
        strspl=str.split() 
        strcopy = str.replace(' ', '\n')
        strcopy = '\n' + strcopy
    thread_name = current_thread().name
    process_name = current_process().name
    queue_s.put(f'Thread {thread_name} in process {process_name} done with result {str_copy} (started with string {str})')
    output.send(str_copy)
    queue_s.put(f'Sent {str_copy} to next thread')   

def server(port_1,port_2):
    queue_s = Queue()
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    thread1=Thread(target=thread_server,args=([HOST,port_1,queue_s]))
    thread2=Thread(target=thread_server,args=([HOST,port_2,queue_s]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    while queue_s.empty() != True:
        item = queue_s.get()
        item = item[2:len(item)-1:]
        item_spl = item.split('|')
        for i in range(len(item_spl)):
            logger.info(item_spl[i])

def thread_server(HOST,PORT,queue_s):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = ' '
            while data :
                data = conn.recv(4096)
                if data:
                    queue_s.put(f"{data}")

if __name__ == '__main__':
    server_log = Process(target=server, args=(PORT_1,PORT_2), daemon=True)
    server_log.start()
    client_1 = Process(target=client, args=(PORT_1,1))
    client_2 = Process(target=client, args=(PORT_2,2))
    client_1.start()
    client_2.start()
    server_log.join()
    client_1.join()
    client_2.join()