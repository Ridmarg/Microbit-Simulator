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

"""This class contains the functionality and variables for a Linked List"""
class LinkedList:
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

    """Add an item to the end of the linked list"""
    def Append(self, data):
        self.length += 1
        # Create new Node
        current = Node(data)
        # Set the Node after current to the current head Node
        current.nextNode = self.head
        # Change current head Node to the current node
        self.head = current

    """Linear search through the linked list"""
    def Search(self, value):
        # Start at the head Node
        current = self.head
        found = False
        # While there is a node and not found value
        while ((current != None) and not(found)):
            if value == current.data:
                found = True
            # Move node forward
            current = current.nextNode
        return found

    """Display the list as a series of print statements"""
    def debugOutput(self):
        current = self.head
        while (current != None):
            print(str(current.data))
            current = current.nextNode

    """Clear the linked list of all values"""
    def Clear(self):
        self.head = None
        self.tail = None
        self.length = 0