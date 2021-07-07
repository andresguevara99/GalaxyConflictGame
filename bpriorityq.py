# Implementation of the bounded Priority Queue ADT using an array of
# queues in which the queues are implemented using a linked list.
from array204 import Array
from llistqueue import Queue

class BPriorityQueue :

  def __init__( self, num_levels = 4 ):
    """Creates an empty bounded priority queue."""
    self._qsize = 0
    self._qlevels = Array( num_levels )
    for i in range( num_levels ) :
      self._qlevels[i] = Queue()

  def is_empty( self ):
    """   # Returns True if the queue is empty."""
    return len( self ) == 0

  def __len__( self ):
    """   # Returns the number of items in the queue."""
    return self._qsize

  def enqueue( self, item, priority ):
    """   # Adds the given item to the queue."""
    assert priority >= 0 and priority < len(self._qlevels), \
           "Invalid priority level."
    self._qlevels[priority].enqueue( item )
    self._qsize += 1

  def dequeue( self ):
    """   # Removes and returns the next item in the queue."""
    # Make sure the queue is not empty.
    assert not self.is_empty(), "Cannot dequeue from an empty queue."

    top_index = self.find_top_priority_queue()
    # We know the queue is not empty, so dequeue from the ith queue.
    self._qsize -= 1
    return self._qlevels[top_index].dequeue()

  def peek( self ):
    """ Return the value of the first queue item without removing it"""
    # Make sure the queue is not empty.
    assert not self.is_empty(), "Cannot peek from an empty queue."
    top_index = self.find_top_priority_queue()
    return self._qlevels[top_index].peek()

  def find_top_priority_queue( self ):
    """ Find the first empty queue in the array """
    # Find the first non-empty queue.
    i = 0
    p = len(self._qlevels)
    while i < p and self._qlevels[i].is_empty() :
      i += 1
    return i
