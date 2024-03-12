# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Install and import libraries
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
import pandas as pd
import numpy as np


# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Storage approximation verteces
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x

class Storage():
  def __init__(self, n, k):
    self.n = n
    self.k = k
    columns = ['number'] + [f'vertex{i}' for i in range(k+1)] + [f'coord{i}' for i in range(1,n+1)]
    self._verteces = pd.DataFrame(columns=columns)
    for i in self._verteces.columns:
      self._verteces[i] = self._verteces[i].astype(int)

    self._vertecesRows = []

    self._hypercubes = pd.DataFrame(columns=['indexSimplex', 'numberHypercube'])
    self._hypercubes['indexSimplex'] = self._hypercubes['indexSimplex'].astype(int)
    self._hypercubes['numberHypercube'] = self._hypercubes['numberHypercube'].astype(int)


  def getVertecesDF(self):
    res =  pd.concat([self._verteces,  pd.DataFrame(self._vertecesRows)], ignore_index=True)
    self._vertecesRows = []
    return res

  def getHypercubesDF(self):
    return self._hypercubes

  def saveSimplexInHypercube(self, simplex, setNumbersHypercube):

    newData = pd.DataFrame([{   'indexSimplex': simplex.getIndex(),
                                'numberHypercube' : numberHypercube}
                                for numberHypercube in setNumbersHypercube ] )

    self._hypercubes = pd.concat([self._hypercubes, newData], ignore_index=True)




  def saveFirstApproximation(self, simplex):
    approximationVertex = simplex.approximationVertex()
    if type(approximationVertex) != np.ndarray:
      return False

    number = simplex.getNumber()
    verteces = simplex.getVerteces()

    newRow = {'number': number}

    for i in range(self.k+1):
        newRow[f'vertex{i}'] = verteces[i]
    for i in range(self.n):
        newRow[f'coord{i+1}'] = approximationVertex[i]

    self._vertecesRows.append(newRow)
    self._verteces = pd.concat([self._verteces,  pd.DataFrame(self._vertecesRows)], ignore_index=True)
    self._vertecesRows = []
    simplex.setIndex(self._verteces.index[-1])
    return True


  def saveApproximation(self, simplex):
    approximationVertex = simplex.approximationVertex()
    if type(approximationVertex) != np.ndarray:
      return False

    number = simplex.getNumber()
    verteces = simplex.getVerteces()

    newRow = {'number': number}
    for i in range(self.k+1):
        newRow[f'vertex{i}'] = verteces[i]
    for i in range(self.n):
        newRow[f'coord{i+1}'] = approximationVertex[i]

    self._vertecesRows.append(newRow)
    simplex.setIndex(self._verteces.index[-1] + len(self._vertecesRows))
    return True