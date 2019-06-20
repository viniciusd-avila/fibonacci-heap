# Implementation of doubly linked list to be used by Fibonacci heap
# by Vinícius D'Avila

class Node:
    def __init__(self,value,key=None,next=None,prev=None):
        self.value = value
        self.next = next
        self.prev = prev
        self.key = value if key is None else key
        
    def __repr__(self):
        return str(self.value)
    
class DoublyLinkedList:
    def __init__(self,head=None):
        self.head=head
        
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next
            
    def push(self,value,key=None):
        node = Node(value,key,self.head)
        if self.head is not None:
            self.head.prev = node
        node.next = self.head
        self.head = node
    
    def __repr__(self):
        node = self.head
        res = '('
        for node in self:
            res += str(node.value) + ' '
        return res[:-1] + ')' if len(res)>1 else res + ')'
            
    def min(self):
        if self.head is None:
            return None
        node = self.head
        min_val = node.key
        min_node = node
        for node in self:
            if min_val > node.key:
                min_val = node.key
                min_node = node
        return min_node.value
    
    def remove(self,value,node=None):
        if node is None:
            node = self.head
        
        if node.value == value:
            if node is self.head:
                self.head = node.next    
            if node.next is not None:
                node.next.prev = node.prev
            if node.prev is not None:
                node.prev.next = node.next
            
        else:
            if node.next is not None:
                return self.remove(value,node.next)