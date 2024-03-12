# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Install and import libraries
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
import queue


# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Simplex queue
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x

class SimplexQueue():

  def __init__(self):
    self._queue = queue.Queue()
    self._recordVertex = {}
    self._cofaces = {}
    self._indexCoface = 0

  def addRecord(self, simplex):
    if simplex.getNumber() in self._recordVertex:
      self._recordVertex[simplex.getNumber()].append(tuple(simplex.getVerteces()))
    else:
      self._recordVertex[simplex.getNumber()] = [tuple(simplex.getVerteces())]

  def inRecord(self, simplex):
    return (simplex.getNumber() in self._recordVertex) and (tuple(simplex.getVerteces()) in self._recordVertex[simplex.getNumber()])

  def enqueue(self, simplex):
    self._queue.put(simplex)

  def dequeue(self):
    return self._queue.get()

  def isEmpty(self):
    return self._queue.empty()