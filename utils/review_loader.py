PRODUCT_ID = 'productId'
USER_ID = 'userId'
PROFILE_NAME = 'profileName'
HELPFULNESS = 'helpfulness'
SCORE = 'score'
TIME = 'time'
SUMMARY = 'summary'
TEXT = 'text'

###################################################
# Static methods to parse a review
###################################################

def get_name_and_value_from_line(line):
  """
  Parse a line to name and value, find split point
  :param line: the line to be parsed, should contain both name and value
  :return: name and value
  """
  split_backslash = line.index('/')
  split_colon = line.index(':')

  name = line[split_backslash + 1: split_colon]
  value = line[split_colon + 1:]
  return name, value


def validate_single_review(review):
  """
  Validates if a single review contains all the required fields.
  :param review: the review to be validated
  :return: if the review is valid
  """
  valid = True
  valid = valid and 'product/{}'.format(PRODUCT_ID) in review
  for item in [USER_ID, PROFILE_NAME, HELPFULNESS, SCORE, TIME, SUMMARY, TEXT]:
    valid = valid and 'review/{}'.format(item) in review
  return valid


def parse_single_review(review_text):
  """
  Parse a paragraph of text to dictionary
  :param review_text: the text to be parsed
  :return: the dictionary of attributes
  """
  lines = review_text.split('\n')[:-1]  # discard the last empty string after \n
  result_dict = {}
  for line in lines:
    try:
      name, value = get_name_and_value_from_line(line)
    except ValueError:
      print('the error is [{}] in: \n{}'.format(line, review_text))
    else:
      result_dict[name] = value

  return result_dict


###################################################
# The review loader class
###################################################
class ReviewLoader:
  def __init__(self, data_path):
    self.data_path = data_path

  def data_iter(self, verbose=False):
    """
    This iterator returns one review each time, with dictionary format:
    {
      productId: pidpidpidpidpid
      userId: uiduiduiduid
      review/profileName: namenamenamename
      review/helpfulness: 7/7
      review/score: 5.0
      review/time: timetime111
      review/summary: summarysummarysummarysummary
      review/text: texttexttexttext
    }
    """
    with open(self.data_path, 'r') as infile:
      paragraph = ''
      counter = 0

      for line in infile:

        if line != '\n' or not (PRODUCT_ID in paragraph and TEXT in paragraph):
          if not line.startswith('product/') and not line.startswith('review/'):
            # this line belongs to previous attr, remove last \n in paragraph
            paragraph = paragraph[:-1]
          paragraph += line

        else:
          # Reachs the end of a paragraph
          # if not validate_single_review(paragraph):
          #   raise ValueError('what what???: [{}]'.format(paragraph))
          review_dict = parse_single_review(paragraph)
          paragraph = ''  # reset the buffer
          counter += 1
          if verbose and counter % 100000 == 0:
            print('Loaded {:,} reviews'.format(counter))

          yield review_dict

      if verbose:
        print('Done, Loaded {:,} reviews in total'.format(counter))