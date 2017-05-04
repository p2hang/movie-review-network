import pickle

from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

from utils.movie_reviews_loader import MovieReviewTextLoader
from utils.tfidf_vector_helper import sparse_matrix_to_dict

review_ids = []


def main():
  in_file_path = 'data/movies.txt'
  feature_name_path = 'data/movie_feature_name.pkl'
  feature_vector_path = 'data/movie_feature_vectors.pkl'

  # for each review
  # loader = ReviewLoader(in_file_path)
  # iterator = loader.review_text_iter

  # for each movie
  loader = MovieReviewTextLoader(in_file_path)
  iterator = loader.data_iter
  get_tfidf_score_and_save(iterator,feature_name_path, feature_vector_path)


def get_tfidf_score_and_save(data_iter, feature_name_path, feature_vector_path):
  """
  Take the in file and parse the text in the review then compute all the tfidf scores,
  save the result in a file
  """
  tokenizer = RegexpTokenizer(r'\w+')
  tokenize = lambda doc: tokenizer.tokenize(doc)
  iterator = text_iter(data_iter)

  # vectorize the texts
  vectorizer = TfidfVectorizer(norm='l2',
                               min_df=20,
                               max_df=0.4,
                               use_idf=True,
                               smooth_idf=False,
                               sublinear_tf=True,
                               decode_error='ignore',
                               tokenizer=tokenize)
  vectors = vectorizer.fit_transform(iterator)
  feature_names = vectorizer.get_feature_names()

  # save feature names
  print('saving feature names...')
  with open(feature_name_path, 'wb') as name_file:
    pickle.dump(feature_names, name_file)

  # save feature vectors
  print('saving feature vectors')
  feature_dict = {}
  counter = 0
  for review_id, feature_vec in zip(review_ids, vectors):
    feature_dict[review_id] = sparse_matrix_to_dict(feature_vec)

    counter += 1
    if counter % 10000 == 0:
      print('Put {:,} features in dict'.format(counter))

  print('saving features to file...')
  with open(feature_vector_path, 'wb') as vector_file:
    pickle.dump(feature_dict,vector_file)
  # check the score of real words
  # print_feature_ranking(features['name'], features['vectors']['B000063W1R_A2M6FIWDCDWDVM'])
  # print(len(feature_names))
  # print(features['vectors'])
  print('Done.')


###########################################################
# Helper Methods
###########################################################
def text_iter(data_iter):
  for text_id, text in data_iter(verbose=True):
    review_ids.append(text_id)
    yield text


if __name__ == '__main__':
  main()
