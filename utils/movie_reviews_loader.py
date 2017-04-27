
from review_loader import ReviewLoader, TEXT, PRODUCT_ID

class MovieReviewTextLoader:
  def __init__(self, data_path):
    self.loader = ReviewLoader(data_path)

  def data_iter(self, verbose):
    pid = None
    review_text = ''
    counter = 0

    for review in self.loader.data_iter(verbose=verbose):
      if pid == None:
        pid = review[PRODUCT_ID]
        review_text = review[TEXT]
      elif pid == review[PRODUCT_ID]:
        review_text += ' ' + review[TEXT]
      else:
        yield pid, review_text
        counter += 1

        if verbose and counter % 10000 == 0:
          print('Loaded review for {:,} movies'.format(counter))

        pid = review[PRODUCT_ID]
        review_text = review[TEXT]


    yield pid, review_text
    counter += 1

    if verbose:
      print('Done, Loaded review for {:,} movies in total'.format(counter))