# Implementation of the Queue ADT using a linked list.
class Queue :
    # Creates an empty queue.
  def __init__( self ):
    self._qhead = None
    self._qtail = None
    self._count = 0
    
   # Returns True if the queue is empty.
  def is_empty( self ):
    return self._qhead is None
    
   # Returns the number of items in the queue.
  def __len__( self ):
    return self._count 
    
   # Adds the given item to the queue.
  def enqueue( self, item ):
    node = _QueueNode( item )
    if self.is_empty() :
      self._qhead = node
    else :
      self._qtail.next = node
      
    self._qtail = node
    self._count += 1
    
   # Removes and returns the first item in the queue.
  def dequeue( self ):
    assert not self.is_empty(), "Cannot dequeue from an empty queue."
    node = self._qhead
    if self._qhead is self._qtail :
      self._qtail = None
      
    self._qhead = self._qhead.next
    self._count -= 1
    return node.item

  # Examine the first item without removing it
  def peek( self ):
    assert not self.is_empty(), "Cannot peek from an empty queue."
    node = self._qhead
    return node.item

# Private storage class for creating the linked list nodes.
class _QueueNode( object ): 
  def __init__( self, item ):
    self.item = item
    self.next = None
