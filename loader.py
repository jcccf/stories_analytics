import networkx as nx

def load_graph(file):
  """Read in a Storeys graph"""
  g = nx.DiGraph()
  mode = "N"
  for l in file:
    l = l.strip()
    if mode == "N":
      if l == "// Nodes":
        mode = "LN"
    elif mode == "LN":
      if l == "// Edges":
        mode = "LE"
      else:  # LOAD NODES
        nparts = l.split(" ", 2)
        g.add_node(int(nparts[0]),
          {'unixtime': int(nparts[1]), 'line': nparts[2]})
        pass
    elif mode == "LE" and len(l) > 0:  # LOAD EDGES
      eparts = [int(x) for x in l.split(" ", 1)]
      g.add_edge(eparts[0], eparts[1])
  return g

if __name__ == '__main__':
  with open("data/graph_000184.log", "r") as f:
    g = load_graph(f)
  for n in g.nodes(data=True):
    print n
  for e in g.edges():
    print e
