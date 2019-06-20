# Implementation of Fibonacci heap by Vinicius D'Avila
# Part of an assignment for the 2019 Discrete Mathematics class, ministered by Luciano Castro (EMAp FGV-RJ)

# Fibonacci heap can be used as a priority queue by Dijkstra's shortest path algorithm
# Heap property: the key of a child node must be greater or equal to the key of its parent node

## Resources
# https://en.wikipedia.org/wiki/Fibonacci_heap
# https://www.cs.princeton.edu/~wayne/teaching/fibonacci-heap.pdf
# https://www.cl.cam.ac.uk/teaching/1415/Algorithms/fibonacci.pdf
# https://www.youtube.com/watch?v=nZ0nFTvQez0
# https://github.com/woodfrog/FibonacciHeap/blob/master/README.md
# https://cs.stackexchange.com/a/7510

from doublylinkedlist import *

class HeapNode:
    # directed graph
    # each parent only points to a single child, each children points to their parent and two of their siblings
    def __init__(self,value,key,degree=0):
        self.parent=None
        self.child=None
        self.right_sibling=None
        self.left_sibling=None
        self.marked=False
        self.degree=degree
        self.value=value
        self.key=key
        
    def __repr__(self):
        parent,child,r_s,l_s = list(map(lambda node: self.__get_value(node),
                                    [self.parent,self.child,self.right_sibling,self.left_sibling]))
        value,key = [self.value,self.key]
        return '\nValue: {value}\nKey: {key}\nParent: {parent}\nChild: {child}\nRight sibling: {r_s}\nLeft sibling: {l_s}\n'.format(
            value=value,key=key,parent=parent,child=child,r_s=r_s,l_s=l_s)
    
    def __get_value(self,node,default=''):
        return node.value if node is not None else default
        
    
class FibonacciHeap:
    def __init__(self):
        self.roots = DoublyLinkedList()
        self.min_root = None
        self.number_of_nodes = 0
        self.dict = {}
    
    def __repr__(self):
        return 'Roots {}\n'.format(self.roots)
    
    def is_empty(self):
        return len(self.roots)==0

    def peek(self):
        return self.min_root
    
    def insert_with_priority(self,value,key):
        node = HeapNode(value,key)
        node.right_sibling = node
        node.left_sibling = node
        self.dict[value] = node
        self.roots.push(node,key)
        self.number_of_nodes += 1
        if self.min_root is None:
            self.min_root = node
        if key < self.min_root.key:
            self.min_root = node
            
            
    def pull_highest_priority_element(self):
        # aka popmin
        # removes the node with the lowest key from the root list
        # places their children in the root list then call cleanup
        
        min_root = self.min_root
        
        self.make_orphans(min_root)
        self.roots.remove(min_root)
        self.cleanup()
        
        try:
            self.min_root = self.roots.min()
        except:
            print('Heap is empty')
        return min_root
            
    def make_orphans(self,node):
        if node.child is not None:
            child = node.child
            while True: # do-while equivalent in Python 
                child.parent = None
                next_child = child.right_sibling
                child.right_sibling = child
                self.roots.push(child,child.key)
                child = next_child
                if child.right_sibling == child:
                    break
            node.child = None
            
    def merge(self,v,u):
        # binomial tree trivial merge
        # places whichever node has the largest key as the child of the other
        if v is None:
            return u
        if u is None:
            return v
        if v.key <= u.key:
            root,child = [v, u]
        else:
            root, child = [u, v]
            
        print(root,child)
            
        if root.child is not None:
            sibling = root.child
            child.right_sibling = sibling.right_sibling
            child.left_sibling = sibling
            sibling.right_sibling = child
        root.child = child
        child.parent = root
        root.degree += 1
        
        print(root,child)
        
        return root
    
    def cleanup(self):
        # merge all roots of same degree
        root_array = [None for i in range(self.number_of_nodes)]
        
        for tree in self.roots:
            t = tree.value
            while root_array[t.degree] is not None:
                u = root_array[t.degree]
                root_array[t.degree] = None
                t = self.merge(t,u)
            root_array[t.degree] = t
        self.roots = DoublyLinkedList()
        for root in root_array:
            if root is not None:
                self.roots.push(root,root.key)
        
    def runaway(self,child,parent):
        if child.right_sibling == child:
            print(child.right_sibling)
            parent.child = None
        else:
            parent.child = child.right_sibling
            child.left_sibling.right_sibling = child.right_sibling
            child.right_sibling.left_sibling = child.left_sibling
        parent.degree -= 1
        child.parent = None
        child.right_sibling = child
        child.marked = False
        self.roots.push(child,child.key)
        
        grandparent = parent.parent
        if grandparent is not None:
            if parent.marked:
                self.runaway(parent,grandparent)
            else:
                parent.marked = True
                
    def decrease_key(self,value,new_key):
        # decrease key then if the heap property is broken,
        # remove node from tree and place it in the root list
        node = self.dict[value]
        node.key = new_key
        parent = node.parent
        if parent is not None and node.key < parent.key:
            self.runaway(node,parent)
        if node.key < self.min_root.key:
            self.min_root = node
