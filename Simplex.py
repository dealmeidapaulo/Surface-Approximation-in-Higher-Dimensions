# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Install and import libraries
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
import numpy as np


# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Auxiliar functions
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x

#O(l)
def psiFunction(elements, number):
  return sum([(elements[j] * (number >> j & 1)) for j in range(len(elements))])

#O(log number)
def binaryRepresentation(number):
  bits = []
  while number>0:
    x = 2**(number.bit_length() -1)
    bits.append(x)
    number -= bits[-1]
  return bits

def basesRepresentation(number, bases):
  if bases.shape[0] == 0:
    return 0

  if bases[-1] <= number:
    return 2**(bases.shape[0]-1) + basesRepresentation(number - bases[-1], bases[:-1])
  else:
    return basesRepresentation(number, bases[:-1])

def simplecesAdjacent(tupleVerteces1, tupleVerteces2):
  return len(set(tupleVerteces1) & set(tupleVerteces2)) == len(tupleVerteces1) -1

def sumSimpleces(tupleVerteces1, tupleVerteces2):
  return tuple(set(tupleVerteces1) | set(tupleVerteces2))

# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Simplex
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x


class Simplex():
  def __init__(self, numberHypercube, verteces, evaluate):
    self._number = numberHypercube
    self._verteces = verteces
    self._dimension = verteces.shape[0] - 1
    self._evaluate = evaluate
    self._dimensionDomain = self.getBases().shape[0]
    self._indexdf = np.nan

  def getNumber(self):
    return self._number
  def getVerteces(self):
    return self._verteces
  def getDimension(self):
    return self._dimension
  def getDimensionDomain(self):
    return self._dimensionDomain
  def getEvaluate(self):
    return self._evaluate
  def getBases(self):
    return self._evaluate.getBases()
  def getIndex(self):
    return self._indexdf

  #O(n)
  def canonicalRepresentation(self):
    s = np.sign(self.getVerteces()[0])
    n = int(abs(self.getVerteces()[0]))
    if n == 0:
      return
    while n>0:
      x = n.bit_length() -1
      self._number += self.getBases()[x] * s
      n -= 2**x
    self._verteces = self._verteces - self._verteces[0]

  #O(n)
  def face(self, numberFace):
    verteces =  np.delete(self.getVerteces(), numberFace)
    res =  Simplex( self.getNumber(),
                    verteces,
                    self.getEvaluate())
    res.canonicalRepresentation()
    return res

  #O(k*n)
  def faces(self):
    return [self.face(i) for i in range(self.getDimension()+1)]


  #O(n**2 k 2**(n-k))
  def cofaces(self):
    gridCoords = self.getEvaluate().gridCoordHypercube(self.getNumber()) #O(n)
    divisions = self.getEvaluate().getDivisions()
    verteces = self.getVerteces()
    bitsDelta = [ binaryRepresentation(int(d))
                  for   d   in  np.diff(verteces)] #O(k * log n-k )
    res  = []
    for numberVertex in range(1,self.getDimension()+1): #O(k)
      for i in range(1, (2**(len(bitsDelta[numberVertex-1])))-1): #O(2** n-k)
        newVertex = verteces[numberVertex-1] + psiFunction(bitsDelta[numberVertex-1], i) #O(n-k)
        a = np.insert(verteces, numberVertex, newVertex) #O(k)
        res.append(Simplex(self.getNumber(), a, self.getEvaluate()))

    bits = binaryRepresentation(int(verteces[-1])) # O(log n-k)
    bits = [2**i  for i in range(self.getDimensionDomain())
                  if (2**i not in bits) and (gridCoords[i] < divisions[i]-1)] #O(n)

    for i in range(1, 2**(len(bits))): #O(2** n-k)
      newVertex =  psiFunction(bits, i) #O(n-k)
      a = Simplex(self.getNumber(),
                  np.append(verteces, verteces[-1]+newVertex),
                  self.getEvaluate())
      res.append(a)

    bits = binaryRepresentation(int(verteces[-1]))
    bits = [2**i  for i in range(self.getDimensionDomain())
                  if (2**i not in bits) and (gridCoords[i] > 0)] #O(n)

    for i in range(1, 2**(len(bits))): #O(2** n-k)
      newVertex =  psiFunction(bits, i) #O(n-k)
      a = Simplex(self.getNumber(),
                  np.insert(verteces, 0, -newVertex),
                  self.getEvaluate()) #O(k)
      a.canonicalRepresentation() #O(n)
      res.append(a)
    return res


  def setIndex(self, i):
    self._indexdf = i

  def approximationVertex(self):
    return self.getEvaluate().approximationVertex(self)
