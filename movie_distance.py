import pickle

from utils.review_loader import ReviewLoader, PRODUCT_ID, USER_ID


def main():
    # build_movie_map_and_save('data/movies.txt', 'data/movie_map.pkl')
    # filter_movie('data/movie_map.pkl', 'data/filtered_movie.pkl')
    compute_distance('data/filtered_movie.pkl', 'data/movies_distance.pkl')


def compute_distance(in_file_path, save_path, verbose=True):
    movies = pickle.load(open(in_file_path, 'rb'))
    count = 0
    distance = {}
    for pid1 in list(movies):
        for pid2 in movies:
            if pid1 != pid2:
                new_id = pid1 + "_" + pid2
                distance[new_id] = movie_distance(movies[pid1], movies[pid2])
                count += 1
                if verbose and count % 1000000 == 0:
                    print('Computed {:,} distance'.format(count))
        movies.pop(pid1)
    pickle.dump(distance, open(save_path, 'wb'))


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
        if len(movie_map[pid]) > 15:
            count += 1
            filtered_movie[pid] = movie_map[pid]
    print("total movies after filter:", count)
    pickle.dump(filtered_movie, open(save_path, 'wb'))


def build_movie_map_and_save(in_file_path, save_path):
    """
    Build a graph from the data
    :param in_file_path: the data to build the graph
    :param save_path: the path to save the nx graph
    """
    loader = ReviewLoader(in_file_path)
    movie_map = {}

    for review in loader.data_iter(verbose=True):

        if review[PRODUCT_ID] not in movie_map:
            movie_map[review[PRODUCT_ID]] = set()
        movie_map[review[PRODUCT_ID]].add(review[USER_ID])

    pickle.dump(movie_map, open(save_path, "wb"))

if __name__ == '__main__':
    main()
