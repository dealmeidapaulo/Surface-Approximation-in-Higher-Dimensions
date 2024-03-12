# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Install and import libraries
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
import numpy as np


# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Evaluate function and resolve linear system
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x


class Evaluate():

  def __init__(self, F, I, K):
    self._dimensionDomain = K.shape[0]
    self._dimensionImage  = F(np.zeros((self._dimensionDomain,1), dtype=int)).shape[0]
    self._pseudoFunction = lambda v : np.append(F(v), np.array([1]), axis=0)
    self._domain = I
    self._divisions = K
    self._perturbationMatrix = np.random.normal(0, (10**-6), size=(self._dimensionDomain, 2**self._dimensionDomain))


    self._bases =  np.empty_like(self._divisions)
    self._bases[0] = 1
    for i in range(1, len(self._divisions)):
      self._bases[i] = self._bases[i-1] * self._divisions[i]



  def getDimensionDomain(self):
    return self._dimensionDomain
  def getDimensionImage(self):
    return self._dimensionImage
  def getPseudoFunction(self):
    return self._pseudoFunction
  def getDomain(self):
    return self._domain
  def getDivisions(self):
    return self._divisions
  def getBases(self):
    return self._bases
  def getPerturbationMatrix(self):
    return self._perturbationMatrix

  def pseudoEvaluate(self, v):
    return self.getPseudoFunction()(v)

  #O(n)
  def gridCoordHypercube(self, numberHypercube):
    K = self.getDivisions()
    n = self.getDimensionDomain()
    res = np.zeros((n,), dtype=int)
    base = np.prod(K[0:-1])
    error_i = numberHypercube

    for i in range(n-1,-1,-1):
      res[i] = error_i // base
      error_i = error_i % base
      base = base // K[i]
    return res

  def hypercubeCoordVertex(self, numberVertex):
    n = self.getDimensionDomain()
    res = np.zeros((n,), dtype=int)
    for i in range(n-1, -1, -1):
      if (numberVertex & (1 << i)):
        res[i] = 1
    return res

  def gridCoordVertexPerturbeted(self, numberHypercube, numberVertex):
    vv = self.hypercubeCoordVertex(numberVertex)
    vh = self.gridCoordHypercube(numberHypercube)
    pert = np.sum(2 ** abs(vv - (vh % 2)))
    res = vv + vh + self.getPerturbationMatrix()[:, pert]
    return res

  def realCoordVertex(self, numberHypercube, numberVertex):
    v = self.gridCoordVertexPerturbeted(numberHypercube, numberVertex)
    I = self.getDomain()
    K = self.getDivisions()
    return ((I[:,1] - I[:,0])/K)*v + I[:,0]

  def linearSystemSolution(self, M):
    k = self.getDimensionImage()
    b = np.zeros((k+1,), dtype=int)
    b[k] = 1
    return np.linalg.solve(M, b)


  def approximationVertex(self, simplex):
    vertecesMatrix = np.column_stack([self.realCoordVertex(simplex.getNumber(), vertex)
                                              for vertex in simplex.getVerteces()])
    evaluationMatrix = np.column_stack([self.pseudoEvaluate(vertex.T)
                                              for vertex in vertecesMatrix.T ] )
    vertexManifold = self.linearSystemSolution(evaluationMatrix)
    if np.any(vertexManifold < 0):
      return np.nan
    vertexManifold = vertecesMatrix @ vertexManifold
    return vertexManifold