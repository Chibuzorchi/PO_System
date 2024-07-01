thread process_order() 
{ 
    while (true) 
    { 
        if (self.queue.length() == 0) 
        { 
            // queue is empty, block until there is at least 1 element 
            sleep(); 
        } 
        order = self.queue.pop(); 
        do_actual_processing(order); 
        // notify the producer that there is space in the queue 
        wakeup(place_order); 
    } 
}
