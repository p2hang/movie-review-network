import ast


def parse_line(line):
  key,value = line.split(':', 1)
  value = ast.literal_eval(value)
  return key,value


class FeatureVecLoader:
  def __init__(self, file_path):
    self.path = file_path

  def load(self, verbose=False):
    result_dict = {}
    count = 0

    with open(self.path, 'r') as file:
      for line in file:
        k,v = parse_line(line)
        result_dict[k] = v
        count += 1

        if verbose and count % 10000 == 0:
          print('Read features for {} movies'.format(count))

    if verbose:
      print('Done. Read features for {} movies in total.'.format(count))
    return result_dict



