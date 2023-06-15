import multiprocessing
import random
import time

class Producer(multiprocessing.Process):
    def __init__(self,queue)