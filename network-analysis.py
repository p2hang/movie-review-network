import pickle

import networkx as nx

from utils.review_loader import ReviewLoader, PRODUCT_ID, USER_ID


def main():
  build_graph_and_save('data/movies.txt', 'data/movie_graph.pkl')


def build_graph_and_save(in_file_path, save_path):
  """
  Build a graph from the data
  :param in_file_path: the data to build the graph
  :param save_path: the path to save the nx graph
  """
  loader = ReviewLoader(in_file_path)
  movie_graph = nx.Graph()

  for review in loader.data_iter(verbose=True):

    if review[PRODUCT_ID] not in movie_graph:
      movie_graph.add_node(review[PRODUCT_ID], type='p')

    if review[USER_ID] not in movie_graph:
      movie_graph.add_node(review[USER_ID], type='u')

  print('total number of nodes: {}'.format(movie_graph.number_of_nodes()))
  pickle.dump(movie_graph, open(save_path, "wb"))

  # Generated graph looks like below
  # total number of nodes: 1142235
  #
  # (' A3GV24GH1AFXDJ', {'type': 'u'})
  # (' B007EMEOEA', {'type': 'p'})
  # (' A2K3MAFGCOZU02', {'type': 'u'})


if __name__ == '__main__':
  main()
