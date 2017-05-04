import pickle

import math

from utils.review_loader import ReviewLoader, PRODUCT_ID, USER_ID, HELPFULNESS, SCORE

FILTER_THRESHOLD = 200
BUCKET_THRESHOLD = 1000


def main():
    build_movie_map_and_save('data/movies.txt', 'data/movie_map_helpfulness_score.pkl')
    filter_movie('data/movie_map_helpfulness_score.pkl', 'data/filtered_movie_score_200.pkl')
    compute_distance('data/filtered_movie_score.pkl', 'data/movies_distance_score.pkl')
    compute_distance('data/filtered_movie.pkl', 'data/movies_distance.pkl')
    bucket_filter('data/movies_distance.pkl_214069086', 'data/bucket_distance.pkl')
    print_distance_from_bucket('data/bucket_distance.pkl', 'data/bucket_distance_100.pkl')


def print_distance_from_bucket(in_file_path, save_path, verbose = True):
    buckets = pickle.load(open(in_file_path, 'rb'))
    distance = {}
    for k in buckets:
        count = 0
        for pid in buckets[k]:
            distance[pid] = buckets[k][pid]
            count += 1
            if count > 100:
                break
    pickle.dump(distance, open(save_path, 'wb'))
    print(distance)


def bucket_filter(in_file_path, save_path, verbose = True):
    distance = pickle.load(open(in_file_path, 'rb'))
    buckets = pickle.load(open(save_path, 'rb'))
    for k in buckets:
        print('bucket {} has {} distances'.format(k, len(buckets[k])))
    count = 0
    for k in distance:
        count += 1
        dis = float(distance[k])
        idx = int(dis * 10 % 10)
        if idx not in buckets:
            buckets[idx] = {}
        if len(buckets[idx]) < BUCKET_THRESHOLD:
            buckets[idx][k] = distance[k]
        if verbose and count % 10000000 == 0:
            print("Scanned {}".format(count))
    for k in buckets:
        print('bucket {} has {} distances'.format(k, len(buckets[k])))
    pickle.dump(buckets, open(save_path, 'wb'))

def compute_distance(in_file_path, save_path, verbose=True):
    movies = pickle.load(open(in_file_path, 'rb'))
    count = 0
    distance = {}
    for pid1 in list(movies):
        for pid2 in movies:
            if pid1 != pid2:
                new_id = pid1 + "_" + pid2
                d = movie_distance_score(movies[pid1], movies[pid2])
                if d != 1:
                    distance[new_id] = d
                count += 1
                if verbose and count % 100000 == 0:
                    print('Computed {:,} distance'.format(count))
                if count % 1000000 == 0:
                    path = save_path + "_" + str(count)
                    print('Saving ' + path)
                    pickle.dump(distance, open(path, 'wb'))
                    distance.clear()
        movies.pop(pid1)
    path = save_path + "_" + str(count)
    pickle.dump(distance, open(path, 'wb'))


def movie_distance_score(map1, map2):
    sum = 0.0
    for uid in map1:
        if uid in map2:
            u1 = compute_score(map1[uid][0], map1[uid][1])
            u2 = compute_score(map2[uid][0], map2[uid][1])
            score = math.sqrt(u1 * u2)
            sum += score
    return sum


def compute_score(h, s):
    s = float(s)
    top, bot = h.split('/')
    h1 = float(top)
    h2 = float(bot) - h1
    score = max(0, (s - 3) * (h1 - h2))
    return score


def movie_distance(set1, set2):
    count = 0.0
    for uid in set1:
        if uid in set2:
            count += 1.0
    jaccard = count / (len(set1) + len(set2) - count)
    distance = 1.0 - jaccard
    return distance


def filter_movie(in_file_path, save_path):
    movie_map = pickle.load(open(in_file_path, 'rb'))
    count = 0
    filtered_movie = {}
    for pid in movie_map:
        if len(movie_map[pid]) > FILTER_THRESHOLD:
            count += 1
            filtered_movie[pid] = movie_map[pid]
    print("total movies after filter:", count)
    pickle.dump(filtered_movie, open(save_path, 'wb'))


def build_movie_map_and_save(in_file_path, save_path):
    loader = ReviewLoader(in_file_path)
    movie_map = {}

    for review in loader.data_iter(verbose=True):
        if review[PRODUCT_ID] not in movie_map:
            movie_map[review[PRODUCT_ID]] = {}
        movie_map[review[PRODUCT_ID]][review[USER_ID]] = (review[HELPFULNESS], review[SCORE])

    pickle.dump(movie_map, open(save_path, "wb"))


if __name__ == '__main__':
    main()
