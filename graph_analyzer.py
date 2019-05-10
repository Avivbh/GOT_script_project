import networkx as nx
import pickle
import csv


class GraphAnalyzer(object):
    def analyze_season(self, graph_pkl_path, season, output_path):
        with open(graph_pkl_path, mode='rb') as season_graph_file:
            season_graphs = pickle.load(season_graph_file)

            results = []

        for episode, graph in season_graphs.items():
            results.append(self._analyze_episode(graph, season, episode))

        self._save_results(results, output_path)

    def _analyze_episode(self, episode_graph, season, episode):
        metrics = {}
        metrics['season'] = season
        metrics['episode'] = episode
        metrics['unique_speakers'] = episode_graph.number_of_nodes()
        # TODO: add more metrics here

        return metrics

    def _save_results(self, results, output_path):
        keys = results[0].keys()
        with open(output_path, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)


if __name__ == '__main__':
    analyzer = GraphAnalyzer()

    season = '2'
    analyzer.analyze_season(f'pickled_graphs/graphs_season_{season}.pkl', season, f'analyze_files/season_{season}_results.csv')
