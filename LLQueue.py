# ---------------------------
# -     Ryan Williamson     -
# - Advanced Higher Project -
# ---------------------------

"""This class contains the data and a pointer to the nextNode"""
class Node:
    """Class Constructor"""
    def __init__(self, data):
        self.data = data
        self.nextNode = None

"""This class contains functionality for a first in first out data structure"""
class Queue:
    """Class Constructor"""
    def __init__(self):
        self.length = 0
        self.head = None
        self.tail = None

    """
    Returns the length of the Linked List using python's built-in
    len() function
    """
    def __len__(self):
        return self.length

    """Adds an item to the queue"""
    def Enqueue(self, data):
        current = Node(data)
        self.length += 1
        # If this is the first Node
        if self.head == None:
            self.head = current
            self.tail = current
        else:
            # Set Node after tail to current
            self.tail.nextNode = current
            # Set new tail to current
            self.tail = current

    """
    Removes an item from the queue and returns the value
    If the queue is empty a node is returned with an empty queue string
    """
    def Dequeue(self):
        if self.head == None:
            return Node("Empty queue")
        # If there is only 1 item in the Queue
        if self.head == self.tail:
            # Store current head Node
            temp = self.head
            # Clear Head and Tail Node
            self.head = None
            self.tail = None
            self.length -= 1
            # Return the stored head node
            return temp
        # When there is more than 1 item in the queue
        temp = self.head
        # Set new head to the Node after the head Node
        self.head = self.head.nextNode
        self.length -= 1
        return temp

    """Display the queue as a series of print's"""
    def debugDisplay(self):
        current = self.head
        while (current != None):
            print(str(current.data))
            current = current.nextNode

    """Converts the queue to a tuple"""
    def convertToTuple(self):
        # Create empty tuple
        tuple = ()
        # Start at the head node
        current = self.head
        # While there is a node to opereate on
        while (current != None):
            tuple = tuple + (current.data, )
            # Move onto next Node
            current=current.nextNode
        return tuple

    """Clear the queue"""
    def clearQueue(self):
        self.head = None
        self.tail = None
