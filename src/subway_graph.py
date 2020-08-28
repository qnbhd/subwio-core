import networkx as nx
import numpy as np

from .cachefy import Cachefy
from .metric import Metric

DIR_FOR_CACHE = 'cache'


class SubwayGraph:

    def __init__(self, city, lines_dict, transitions):
        self.city = city
        self.lines_dict = lines_dict
        self.transitions = transitions

        self.flatted_stations_list = self.flat(lines_dict)
        self.station_name_idx_dict = {value.subway_name: key for key, value in enumerate(self.flatted_stations_list)}

        self.adj = np.zeros((len(self), len(self)))

        self.calculate_weights()

        self.__setup_transitions_on_adj()

        self.__G = nx.from_numpy_matrix(self.adj, create_using=nx.DiGraph())

        self.sorted_all_pairs_paths_length = self.get_weighted_transitive_closure()
        self.sorted_all_pairs_paths = self.get_all_pair_paths()

    @Cachefy.cache_dict_of_dicts(DIR_FOR_CACHE)
    def get_weighted_transitive_closure(self):
        all_pairs_dij_len = dict(nx.all_pairs_dijkstra_path_length(self.__G))
        sorted_all_pairs_paths_length = {key: dict(sorted(value_dict.items(), key=lambda x: int(x[0]))) for
                                         key, value_dict in all_pairs_dij_len.items()}
        return sorted_all_pairs_paths_length

    @Cachefy.cache_dict_of_dicts(DIR_FOR_CACHE)
    def get_all_pair_paths(self):
        all_pairs_dij = dict(nx.all_pairs_dijkstra_path(self.__G))
        sorted_all_pair_path = {key: dict(sorted(value_dict.items(), key=lambda x: int(x[0]))) for
                                key, value_dict in all_pairs_dij.items()}
        return sorted_all_pair_path

    def get_len_and_path_between_stations(self, name1, name2):
        return self.get_path_len_between_stations(name1, name2), \
               self.get_path_between_stations(name1, name2)

    def get_path_between_stations(self, name1, name2) -> list:
        idx1 = self.get_idx_by_name(name1)
        idx2 = self.get_idx_by_name(name2)
        return self.sorted_all_pairs_paths[idx1][idx2]

    def get_path_len_between_stations(self, name1, name2) -> float:
        idx1 = self.get_idx_by_name(name1)
        idx2 = self.get_idx_by_name(name2)
        return self.sorted_all_pairs_paths_length[idx1][idx2]

    def get_train_mean_speed(self):
        return self.dummy_speed()

    @staticmethod
    def dummy_speed():
        return 40

    def calculate_mean_time(self, length):
        mean_time = length * 1000 / (self.get_train_mean_speed() / 3.6)
        return mean_time

    def __len__(self):
        return len(self.flatted_stations_list)

    def get_distance_between_stations(self, station1_name, station2_name):
        return self.adj[self.get_idx_by_name(station1_name)][self.get_idx_by_name(station2_name)]

    @staticmethod
    def create_np_matrix(n: int, m: int, filler=0) -> np.ndarray:
        matrix = np.zeros((n, m))
        for i in range(n):
            for j in range(m):
                matrix[i][j] = filler
        return matrix

    @staticmethod
    def create_square_matrix(n: int, main_filler=0, diagonal_filler=0):
        matrix = SubwayGraph.create_np_matrix(n, n, main_filler)
        for i in range(n):
            matrix[i][i] = diagonal_filler
        return matrix

    def get_idx_by_name(self, name):
        return self.station_name_idx_dict[name]

    def __setup_transitions_on_adj(self):
        for transition in self.transitions:
            idx1 = self.get_idx_by_name(transition.subway1)
            idx2 = self.get_idx_by_name(transition.subway2)
            self.adj[idx1][idx2] = self.adj[idx2][idx1] = 0.0001

    @staticmethod
    def flat(lines_dict):
        flatted = []
        for line, line_stations in lines_dict.items():
            for i in range(len(line_stations)):
                flatted.append(line_stations[i])
        return flatted

    def calculate_weights(self):
        idx = 1
        for line_name, line_stations in self.lines_dict.items():
            for i in range(1, len(line_stations)):
                station1 = line_stations[i]
                station2 = line_stations[i - 1]
                dist = Metric.metric(station1.point, station2.point)
                self.adj[idx][idx - 1] = self.adj[idx - 1][idx] = dist
                idx += 1
            idx += 1
