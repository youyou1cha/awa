from threading import Thread
from time import sleep

class CookBook(Thread):
    def __init__(self)->None:
        Thread.__init__(self)
        self.message = "Hello Parallel Python CookBook\n"

    def print_message(self):
        print(self.message)

    def run(self):
        print("Thread Starting\n")
        x = 0
        while (x < 10):
            self.print_message()
            sleep(2)
            x += 1
        print("Thread Eende\n")

print("Process started")

helloPython = CookBook()
helloPython.start()

print("Process Ended")