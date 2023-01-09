import heapq

# Edited implementation of PriorityQueue with a decrease key function built in
class PriorityQueue:

    # Constructor
    def __init__(self):
        # The heap
        self.arr = []
        # The dictionary for seen
        self.seen = {}

    # Get Min Function
    def top(self):
        return self.arr[0]

    # Remove Min
    def pop(self):
        heapq.heappop(self.arr)

    # Add element
    def push(self, key, val):
        heapq.heappush(self.arr, (val, key))

    # Decrease Key
    def decreaseKey(self, key, val): 
        i = 0
        while (i < len(self.arr)):
            if key == self.arr[i][1]:
                self.arr[i] = (val, key)
                heapq.heapify(self.arr)
                return True
            i += 1
        return False
    
    # (FOR TESTING) Prints the heap
    def printHeap(self):
        print(self.arr)