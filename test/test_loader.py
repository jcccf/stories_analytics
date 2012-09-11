from .. import loader
import unittest, os


class TestLoader(unittest.TestCase):

  def setUp(self):
    self.file = os.tmpfile()
    str = """
      // Nodes
      1 100 Hello world
      2 400 Bye everyone!
      // Edges
      1 2
      """
    self.file.write(str)
    self.file.seek(0)

  def test_loader(self):
    g = loader.load_graph(self.file)
    self.assertEqual(len(g.nodes()), 2)
    self.assertEqual(g.node[1]['line'], "Hello world")
    self.assertEqual(g.node[2]['unixtime'], 400)
    self.assertEqual(len(g.edges()), 1)
