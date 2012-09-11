from networkx import *
try:
    import numpy.linalg
    eigenvalues=numpy.linalg.eigvals
except ImportError:
    raise ImportError("numpy can not be imported.")

try:
    from pylab import *
except:
    pass

n = 1000  # 1000 nodes
m = 5000  # 5000 edges

G = gnm_random_graph(n, m)

G2 = star_graph(10)
G3 = star_graph(100)
G4 = path_graph(100)
G5 = complete_graph(100)

g1 = Graph()
g1.add_edge(1, 2)
g1.add_edge(2, 3)
g1.add_edge(2, 4)
g1.add_edge(1, 5)
g1.add_edge(5, 6)
g1.add_edge(5, 7)
g1.add_edge(1, 8)
g1.add_edge(8, 9)
g1.add_edge(8, 10)
g15 = Graph()
g15.add_edge(1, 2)
g15.add_edge(2, 3)
g15.add_edge(2, 4)
g15.add_edge(1, 5)
g15.add_edge(5, 6)
g15.add_edge(5, 7)
g2 = star_graph(10)
g3 = path_graph(10)

def get_eigenvalues(G):
  L = normalized_laplacian(G)
  e = eigenvalues(L)
  # print sorted(e, reverse=True)[0], sorted(e, reverse=True)[1]
  print sorted(e)[1]
  # print("Largest eigenvalue:", max(e))
  # print("Smallest eigenvalue:", min(e))

# get_eigenvalues(G)
# get_eigenvalues(G2)
# get_eigenvalues(G3)
# get_eigenvalues(G4)
# get_eigenvalues(G5)
get_eigenvalues(g1)
get_eigenvalues(g15)
get_eigenvalues(g2)
get_eigenvalues(path_graph(10))
get_eigenvalues(path_graph(22))