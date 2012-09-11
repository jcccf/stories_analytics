import networkx as nx
import pygraphviz as pgv
from mtools import *
from mtools import mplot
from loader import *
from temporal import *
import glob
import os.path


if __name__ == '__main__':

  leafs = []
  reachs = []
  labels = []
  mapping = {315: 0, 184: 3, 246: 3, 318: 3,
    432: 1, 433: 1, 508: 1, 533: 1, 606: 1,
    625: 1, 456: 2, 509: 2, 574: 2, 626: 2}
  colormap = ['r', 'g', 'b', 'y']

  print "Id Mapping NumNodes MaxDepth RootDegreeCentNorm " + \
    "RootClosenessCentNorm AvgPathLength PropLeaves AvgLeafDepth " + \
    "Diameter Radius PropAddedToLeaf AlgebraicConnectivity " + \
    "AverageNumWords"

  time_diff_2s, min_after_2s = [], []

  for filename in glob.glob("data/graph_*.log"):
    filebase = os.path.basename(filename).split(".")[0]
    graphid = int(filebase.split("_")[1])
    labels.append(str(graphid))
    with open(filename, "r") as f:
      g = load_graph(f)

    ug = g.to_undirected()

    depth = mgraph.directed.depth(g)
    roots = mgraph.directed.roots(g)
    root_centrality = mgraph.directed.degree_centrality(g, roots[0])
    root_closeness_centrality = nx.closeness_centrality(ug)[roots[0]]
    average_path_length = nx.average_shortest_path_length(ug)

    depths = mgraph.directed.depths(g)
    leaves = mgraph.directed.leaves(g)
    leaf_depths = [depths[l] for l in leaves]
    average_leaf_depth = float(sum(leaf_depths)) / len(leaf_depths)

    reaches = mgraph.directed.reach(g, roots[0])
    reachs.append(mgroup.dict.percentage(reaches))

    num_nodes = len(g.nodes())
    prop_leaves = (len(leaves) - 0.0) / num_nodes
    diameter = nx.diameter(ug)
    radius = nx.radius(ug)
    algebraic_connectivity = mgraph.undirected.algebraic_connectivity(ug)

    # Print only lines along longest branch
    # max_node = max(depths, key=depths.get)
    # curr_node = [max_node]
    # while len(curr_node) > 0:
    #   print g.node[curr_node[0]]['line']
    #   curr_node = g.predecessors(curr_node[0])

    # for n, data in g.nodes_iter(data=True):
    #   print data['line']

    import nltk
    lines = [data['line'] for n, data in g.nodes_iter(data=True)]
    word_lengths = [len(nltk.word_tokenize(l)) for l in lines]
    avg_word_length = (sum(word_lengths) - 0.0) / len(word_lengths)

    edges = edges_temporal(g)
    is_leaf = is_leaf_temporal(edges)
    is_leaf_ints = [int(i[0]) for i in is_leaf]
    leafs.append(is_leaf_ints)
    mplot.one.p("plots/%s_leaf.svg" % filebase, is_leaf_ints)

    prop_add_leaf = (sum(is_leaf_ints) - 0.0) / num_nodes

    a = pgv.AGraph(directed=True)
    for u, v in g.edges_iter():
      a.add_edge(u, v)
    a.layout()
    a.draw('graphs/%s.png' % filebase)

    with open('data/temporal_lines/%s.txt' % filebase,  'w') as f:
      for (u, v), time in edges_temporal(g):
        f.write("%d\t%s -> %s\n" % (time, g.node[u]['line'],
          g.node[v]['line']))

    with open('data/temporal_lines_2/%s.txt' % filebase, 'w') as f:
      for n, times, time_diff, time_diff_2, miny, min_after_2 in edges_temporal_2(g):
        if mapping[graphid] == 1 or mapping[graphid] == 2:
          time_diff_2s.append(time_diff_2)
          if miny < 999999999: min_after_2s.append(min_after_2)
        f.write("%s\n\t%s -> %s %s\n\t%s %s\n" % (g.node[n]['line'], times, time_diff, time_diff_2, miny, min_after_2))

    print graphid, mapping[graphid], num_nodes, depth, root_centrality, \
      root_closeness_centrality, average_path_length, prop_leaves, \
      average_leaf_depth, diameter, radius, prop_add_leaf, \
      algebraic_connectivity, avg_word_length

  colors = [colormap[mapping[int(i)]] for i in labels]
  mplot.many.p("plots/many.png", leafs, sliding=10, title='Leaf addition',
    xlabel="Nth node added", ylabel="Added to leaf?",
    labels=labels, color=colors)
  mplot.many.p("plots/reaches.png", reachs, title='Reach',
    xlabel="Steps out", ylabel="% of nodes",
    labels=labels, color=colors)

  import numpy
  print "Median time between addition of first 2 children to a node with at least 2 children", numpy.median(time_diff_2s)
  print "The mean time instead, and the proportion where the first node added to a child happened after the first 2 children were added to a parent node"
  print (sum(time_diff_2s) - 0.0) / len(time_diff_2s), (sum(min_after_2s) - 0.0) / len(min_after_2s)
