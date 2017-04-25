import pickle

from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

from utils.review_loader import ReviewLoader, TEXT, PRODUCT_ID, USER_ID


def text_loader(data_iter):
  for review in data_iter(verbose=True):
    yield review[TEXT]


def main():
  in_file_path = 'data/movies.txt'
  save_path = 'data/review_text_features.pkl'
  get_tfidf_score_and_save(in_file_path, save_path)


def get_tfidf_score_and_save(in_file_path, save_path):
  """
  Take the in file and parse the text in the review then compute all the tfidf scores,
  save the result in a file
  """
  tokenizer = RegexpTokenizer(r'\w+')
  tokenize = lambda doc: tokenizer.tokenize(doc)
  loader = ReviewLoader(in_file_path)
  text_iter = text_loader(loader.data_iter)

  # vectorize the texts
  vectorizer = TfidfVectorizer(norm='l2', min_df=0,
                               use_idf=True,
                               smooth_idf=False,
                               sublinear_tf=True,
                               decode_error='ignore',
                               tokenizer=tokenize)
  vectors = vectorizer.fit_transform(text_iter)
  feature_names = vectorizer.get_feature_names()

  # put feature names and vectors in a dictionary
  features = {'name': feature_names, 'vectors': {}}
  for review, feature_vec in zip(loader.data_iter(verbose=True), vectors):
    features['vectors'][get_review_id(review[PRODUCT_ID], review[USER_ID])] = feature_vec

  # save features to a file
  pickle.dump(features, open(save_path, "wb"))

  # check the score of real words
  # print_feature_ranking(features['name'], features['vectors']['B000063W1R_A2M6FIWDCDWDVM'])


###########################################################
# Helper Methods
###########################################################
def get_review_id(product_id, user_id):
  """
  Get id for a review with product id and user id
  """
  return '{}_{}'.format(product_id, user_id)


def sparse_matrix_to_list(sparse_matrix):
  """
  Transform tfidf sparse matrix to a list of tuples(index, score)
  """
  matrix_as_list = sparse_matrix.todense().tolist()[0]
  score_list = [pair for pair in zip(range(len(matrix_as_list)), matrix_as_list) if pair[1] > 0]
  return score_list


def print_feature_ranking(feature_names, vector):
  """
  print the word and score of the word in descending order.
  :param feature_names: the mapping between index and word
  :param vector: the sparse matrix contains the scores
  """
  feature_list = sparse_matrix_to_list(vector)
  feature_list = sorted(feature_list, key=lambda t: t[1] * -1)
  for word, score in [(feature_names[word_id], score) for (word_id, score) in feature_list]:
    print('{0: <20} {1}'.format(word, score))


if __name__ == '__main__':
  main()
