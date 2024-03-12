# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x
# Save .pol
# ------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x------------------------------------------x


def savePol(CS, E):
    with open('output.pol', 'w') as f:
      f.write(str(E.getDimensionDomain()) + ' ' + str(E.getDimensionImage()) + '\n')
      f.write(' '.join([str(x) for x in E.getDivisions()]) + '\n\n')
    
      for hypercube in CS:
        f.write(' '.join([str(x)  for x in hypercube[-1][0]]) + '\n')
        f.write('1\n')
        f.write(f'{len(hypercube[0])}\n')
        for vertex in hypercube[0]:
          f.write('  '.join([str(x+1) for x in vertex[0]]) + ' ' +
                  '  '.join([f'{x:.16f}' for x in vertex[1]]) + '\n')
    
        for i in range(1,len(hypercube)-1):
          f.write(str(len(hypercube[i])))
          for connection in hypercube[i]:
            f.write('\n')
            f.write('  '.join([str(x) for x in connection]))
          f.write('\n')
        f.write('\n')
      f.write('-1')