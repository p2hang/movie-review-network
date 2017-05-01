import pickle
import matplotlib.pyplot as plt
import time
from utils.feature_vec_loader import FeatureVecLoader
from scipy.stats import pearsonr


def main():
  calculate_dist_vs_score()


def calculate_dist_vs_score():
  start = time.time()
  ##########
  # load movie feature
  loader = FeatureVecLoader('data/movie_feature_vectors.txt')
  feature_dict = loader.load(verbose=True)
  print('Done loading feature dict in {}'.format(time.time() - start))


  #########
  # load movie distance
  dist = []
  similarity = []
  count = 0
  with open('data/movies_distance/movies_distance.pkl_50000000', 'rb') as file:
    dist0 = pickle.load(file)
    print('Done loading movie distance in {}'.format(time.time() - start))

    for k, v in dist0.items():
      dist.append(v)
      k1, k2 = k.split('_')
      similarity.append(product_sparse_dict(feature_dict[k1], feature_dict[k2]))
      count += 1

      if count % 1000 == 0:
        print(count)

      if count == 100000:
        break

  print('p-value is {}'.format(pearsonr(dist,similarity)))
  #############
  # plot everything
  axes = plt.gca()
  axes.set_xlim([0, 0.5])
  axes.set_ylim([0.7, 1.00])
  plt.scatter(similarity, dist)
  plt.show()





def product_sparse_dict(vec1, vec2):
  score = 0
  for k, v, in vec1.items():
    if k in vec2:
      score += v * vec2[k]

  return score


if __name__ == '__main__':
  main()