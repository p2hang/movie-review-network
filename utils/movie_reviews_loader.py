import pickle

from utils.review_loader import ReviewLoader, TEXT, PRODUCT_ID, HELPFULNESS


def helpfulness_to_decimal(helpfulness_str):
  upvote,total = helpfulness_str.split('/')
  if upvote == '0' and total == '0':
    return 1
  else:
    return float(upvote) / float(total)


class MovieReviewTextLoader:
  def __init__(self, data_path):
    self.loader = ReviewLoader(data_path)

  def data_iter(self, verbose, min_num=99):
    with open('data/movie_review_count.pkl', 'rb') as file:
      count_map = pickle.load(file)
    id_text_dict = {}


    for review in self.loader.data_iter(verbose=verbose):
      pid = review[PRODUCT_ID]
      helpfulness = helpfulness_to_decimal(review[HELPFULNESS])

      if count_map[pid] >= min_num and helpfulness > 0.6 :
        if pid not in id_text_dict:
          id_text_dict[pid] = ''

        id_text_dict[pid] += review[TEXT] +' '


    # generator for built dictionary
    for id,text in id_text_dict.items():
      yield id, text


