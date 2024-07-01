import pytest
import threading
from purchaseSystem import MAX_QUEUE_SIZE, PurchaseOrderSystem, place_order_thread, process_order_thread

@pytest.fixture
def order_system():
    return PurchaseOrderSystem()

def test_concurrent_ordering(order_system):
    threads = []
    for i in range(6):  # more than MAX_QUEUE_SIZE to test full queue behavior
        t = threading.Thread(target=place_order_thread, args=(order_system, f"order_{i}"))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert order_system.queue.qsize() == MAX_QUEUE_SIZE  

def test_concurrent_processing(order_system):
    # First, fill the queue
    for i in range(MAX_QUEUE_SIZE):
        order_system.place_order(f"order_{i}")

    threads = []
    results = []

    def process_and_store_result(order_system):
        result = process_order_thread(order_system)
        results.append(result)

    for _ in range(MAX_QUEUE_SIZE):
        t = threading.Thread(target=process_and_store_result, args=(order_system,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(results) == MAX_QUEUE_SIZE  
    assert order_system.queue.qsize() == 0 

def test_mixed_operations(order_system):
    threads = []

    # Create threads for placing orders
    for i in range(6):
        t = threading.Thread(target=place_order_thread, args=(order_system, f"order_{i}"))
        threads.append(t)

    # Create threads for processing orders
    for _ in range(6):
        t = threading.Thread(target=process_order_thread, args=(order_system,))
        threads.append(t)

    # Start all threads
    for t in threads:
        t.start()

    # Join all threads
    for t in threads:
        t.join()

    assert order_system.queue.qsize() == 0  
