def sparse_matrix_to_dict(sparse_matrix):
  """
  Transform tfidf sparse matrix to a dictionary
  """
  dok = sparse_matrix.todok()
  vec_dict = {}
  for k, v in dok.items():
    vec_dict[k[1]] = round(v, 3)
  return vec_dict


def print_feature_ranking(feature_names, vector):
  """
  print the word and score of the word in descending order.
  :param feature_names: the mapping between index and word
  :param vector: the sparse matrix contains the scores
  """
  feature_list = sorted(vector, key=lambda t: t[1] * -1)
  for word, score in [(feature_names[word_id], score) for (word_id, score) in feature_list]:
    print('{0: <20} {1}'.format(word, score))


def get_review_id(product_id, user_id):
  """
  Get id for a review with product id and user id
  """
  return '{}_{}'.format(product_id, user_id)