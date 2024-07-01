import threading
from queue import Queue

MAX_QUEUE_SIZE = 6

class PurchaseOrderSystem:
    def __init__(self):
        self.queue = Queue(maxsize=MAX_QUEUE_SIZE)
        self.condition = threading.Condition()

    def place_order(self, order):
        with self.condition:
            while self.queue.full():
                self.condition.wait()
            self.queue.put(order)
            self.condition.notify_all()

    def process_order(self):
        with self.condition:
            while self.queue.empty():
                self.condition.wait()
            order = self.queue.get()
            self.condition.notify_all()
            return order

order_system = PurchaseOrderSystem()

def place_order_thread(order_system, order_data):
    order_system.place_order(order_data)

def process_order_thread(order_system):
    return order_system.process_order()
