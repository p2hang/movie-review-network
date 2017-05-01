
from review_loader import ReviewLoader, TEXT, PRODUCT_ID

class MovieReviewTextLoader:
  def __init__(self, data_path):
    self.loader = ReviewLoader(data_path)

  def data_iter(self, verbose, min_num=99):
    pid = None
    review_text = ''
    counter_total = 0
    counter_movie = 0

    for review in self.loader.data_iter(verbose=verbose):
      if pid == None:
        pid = review[PRODUCT_ID]
        review_text = review[TEXT]
      elif pid == review[PRODUCT_ID]:
        review_text += ' ' + review[TEXT]
      else:
        if counter_movie >= min_num:
          yield pid, review_text
          counter_total += 1
          counter_movie = 0

          if verbose and counter_total % 500 == 0:
            print('Loaded review for {:,} movies'.format(counter_total))

        pid = review[PRODUCT_ID]
        review_text = review[TEXT]

      # increment the counter for current pid
      counter_movie += 1


    yield pid, review_text
    counter_total += 1

    if verbose:
      print('Done, Loaded review for {:,} movies in total'.format(counter_total))