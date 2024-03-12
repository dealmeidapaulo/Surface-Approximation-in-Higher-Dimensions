# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Install and import libraries
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
import numpy as np
import concurrent.futures

from Simplex import Simplex
from Evaluate import Evaluate
from SimplexQueue import SimplexQueue
from Storage import Storage
from SavePolytope import savePol




# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Auxiliar functions
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x

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




  


if __name__ == '__main__':

    F = lambda x: np.array([ x[0]**2 + x[1]**2 - 0.25,
                            x[2]**2 + x[3]**2 - 1])
    
    I = np.array([[-1.5,1.5], [-1.5,1.5], [-1.5,1.5], [-1.5,1.5]])
    K = np.array([10]*4)

    
    
    
    E = Evaluate(F,I,K)
    initialSimplex = Simplex(5833, np.array([ 0, 3, 7]), E)
    
    SQ = SimplexQueue()
    
    S = Storage(E.getDimensionDomain(), E.getDimensionImage())
    
    S.saveFirstApproximation(initialSimplex)
    SQ.addRecord(initialSimplex)
    SQ.enqueue(initialSimplex)    

# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Approximation Vertices
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
  
    
    while not SQ.isEmpty():
      simplex = SQ.dequeue()
      simpleces = simplex.cofaces()
      numbers = {s.getNumber() for s in simpleces}
      S.saveSimplexInHypercube(simplex, numbers)
    
      simpleces = sum([element.faces() for element in simpleces], [])
    
      for x in simpleces:
        if (not SQ.inRecord(x)) and S.saveApproximation(x):
          SQ.enqueue(x)
          SQ.addRecord(x)
    

# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Combinatorial Skeleton
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
    CS = []
    
    
    hypercubes = S.getHypercubesDF()
    verteces = S.getVertecesDF()
    
    k = E.getDimensionImage()
    n = E.getDimensionDomain()
    
    vertecesCols = [f'vertex{j}' for j in range(k+1)]
    coordCols = [f'coord{j}' for j in range(1, n+1)]
    
    
    for numberHypercube in hypercubes['numberHypercube'].unique():    

      CShypercube = [[] for i in range((n-k) +2)]

      indices = hypercubes[hypercubes['numberHypercube'] == numberHypercube]['indexSimplex']
      vertecesHypercube = verteces.loc[indices]
      vertecesHypercube = vertecesHypercube.reset_index(drop=True)
      for i in range(k+1):
        vertecesHypercube[f'vertex{i}'] = vertecesHypercube[f'vertex{i}'] + vertecesHypercube['number'].apply(lambda num: basesRepresentation(num - numberHypercube, E.getBases()))
      vertecesHypercube = vertecesHypercube.drop('number', axis=1)
      vertecesHypercube['Index'] = range(1, len(vertecesHypercube) + 1)


      x = vertecesHypercube[vertecesCols].values.astype(int)
      y = vertecesHypercube[coordCols].values

      faces = dict(zip(map(tuple, x), vertecesHypercube.Index.astype(int)))
      CShypercube[0] = list(zip(map(tuple, x), map(tuple, y)))

      step = 1
      while step < (n-k+1):
        cofaces = {}
        index = 1
        for pair in [(i, j) for j in faces for i in faces if i<j]:
          if simplecesAdjacent(pair[0],pair[1]):
            x = sumSimpleces(pair[0],pair[1])
            if not x in cofaces:
              cofaces[x] = index
              index += 1
              CShypercube[step].append((faces[pair[0]], faces[pair[1]]))
            CShypercube[step][cofaces[x]-1] = tuple( set( CShypercube[step][cofaces[x]-1] + (faces[pair[0]], faces[pair[1]]) ) )
        faces = cofaces.copy()
        step += 1
      CShypercube[-1] = [(numberHypercube,) + tuple(E.gridCoordHypercube(numberHypercube))]

      CS.append(CShypercube)
      
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Save .pol
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
    savePol(CS, E)