import pickle
import time

import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from utils.tfidf_vector_helper import print_feature_ranking


def main():
  calculate_dist_vs_score()
  # show_feature_ranking()




def show_feature_ranking():
  with open('data/movie_feature_vectors.pkl', 'rb') as file:
    feature_dict = pickle.load(file)
  with open('data/movie_feature_name.pkl', 'rb') as file:
    feature_name = pickle.load(file)

  count = 0
  for k,v in feature_dict.items():
    print_feature_ranking(feature_name, v)
    count += 1

    if count == 5:
      break


def calculate_dist_vs_score():
  start = time.time()
  ####################################
  # load movie feature
  with open('data/movie_feature_vectors.pkl', 'rb') as file:
    feature_dict = pickle.load(file)

  print('Done loading feature dict in {}s'.format(time.time() - start))


  #####################################
  # load movie distance
  dist = []
  similarity = []
  count = 0
  with open('data/movies_distance/movies_distance.pkl_50000000', 'rb') as file:
    dist0 = pickle.load(file)
    print('Done loading movie distance in {}s'.format(time.time() - start))

    for k, v in dist0.items():
      if v < 0.75:
        continue
      dist.append(v)
      k1, k2 = k.split('_')
      similarity.append(product_sparse_dict(feature_dict[k1], feature_dict[k2]))
      count += 1

      if count % 1000 == 0:
        print(count)

      if count == 500000:
        break

  print('p-value is {}'.format(pearsonr(dist,similarity)))
  ####################################################
  # plot everything
  axes = plt.gca()
  # axes.set_xlim([0, 0.3])
  # axes.set_ylim([0, 500])
  plt.scatter(similarity, dist)
  plt.xlabel('similarity')
  plt.ylabel('distance')
  plt.show()





def product_sparse_dict(vec1, vec2):
  score = 0
  for k, v, in vec1.items():
    if k in vec2:
      score += v * vec2[k]

  return score


if __name__ == '__main__':
  main()