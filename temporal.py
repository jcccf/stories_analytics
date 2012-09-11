import networkx as nx


def edges_temporal(dg):
  '''Return a list of (edge, time since earliest node) tuples in order of
  addition to the graph'''
  # For each edge, link to node which came later
  for u, v in dg.edges_iter():
    if dg.node[u]['unixtime'] > dg.node[v]['unixtime']:
      dg.node[u].setdefault('edges', set()).add((u, v))
    else:
      dg.node[v].setdefault('edges', set()).add((u, v))

  # Order nodes in temporal order
  nodes = sorted(dg.nodes(data=True), key=lambda x: x[1]['unixtime'])
  # print nodes
  edges = []
  basetime = nodes[0][1]['unixtime']  # time 0
  for n, data in nodes:
    if 'edges' in data:
      edges += [(e, data['unixtime'] - basetime) for e in data['edges']]
  return edges


def edges_temporal_2(dg):
  '''Really hacky way to get the times at which children were added to a node,
  the time difference between the first 2 children, and the time at which
  a node was added to a child and whether that happened after the first 2
  children of the parent node were added'''
  # For each edge, link to node which came later
  for u, v in dg.edges_iter():
    dg.node[u].setdefault('edgeslater', set()).add((u, v))

  # Order nodes in temporal order
  nodes = sorted(dg.nodes(data=True), key=lambda x: x[1]['unixtime'])
  # print nodes
  edges = []
  basetime = nodes[0][1]['unixtime']  # time 0
  for n, data in nodes:
    if 'edgeslater' in data:
      edges_sorted = sorted([(e, dg.node[e[1]]['unixtime'] - basetime) for e in data['edgeslater']], key=lambda x: x[1])
      if len(edges_sorted) > 1:
        times = [t for e, t in edges_sorted]
        time_diff = edges_sorted[-1][1] - edges_sorted[0][1]
        time_diff_2 = edges_sorted[1][1] - edges_sorted[0][1]
        time_first_add = [999999999]
        for _, v in data['edgeslater']:
          if 'edgeslater' in dg.node[v]:
            time_first_add.append(sorted([(e,dg.node[e[1]]['unixtime'] - basetime) for e in dg.node[v]['edgeslater']], key=lambda x: x[1])[0][1])
        time_first_add = min(time_first_add)
        time_first_add_after_2 = time_first_add > edges_sorted[1][1]
        edges.append((n, times, time_diff, time_diff_2,
          time_first_add, time_first_add_after_2))

  return edges


def is_leaf_temporal(edgelist):
  '''Return (boolean, time) tuples whose values depend on whether the newest
  node added was added to a leaf node or not'''
  leafseq = []
  dg = nx.DiGraph()
  for (u, v), unixtime in edgelist:
    if not (u in dg and v in dg):
      if u in dg:  # v added after u
        leafseq.append((dg.out_degree(u) > 0, unixtime))
      elif v in dg:  # u added after v, impossible with current implementation
        raise Exception("Not possible that %s was added after %s!" % (u, v))
      else:  # Initial 2 nodes, ignore first node
        leafseq.append((True, unixtime))
    dg.add_edge(u, v)
  return leafseq
