import pickle
import networkx as nx
from collections import defaultdict
from common import Tokens


class GraphCreator(object):
    def __init__(self, scenes_file_path):
        self._scenes = self._open_scenes(scenes_file_path)
        self._create_episodes_graphs()
        self._episodes_graphs = self._create_episodes_graphs()

    def export_episode_graph_to_gephi(self, episode, file_path):
        nx.write_gexf(self._episodes_graphs[episode], file_path)

    def pickle_season_graphs(self, file_path):
        with open(file_path, mode='wb') as graphs_file:
            pickle.dump(self._episodes_graphs, graphs_file)

    def _open_scenes(self, scenes_file_path):
        with open(scenes_file_path, mode='rb') as scenes_file:
            return pickle.load(scenes_file)

    def _create_episodes_graphs(self):
        episode_to_scenes = defaultdict(list)
        for scene in self._scenes: episode_to_scenes[scene._episode].append(scene)
        graphs = {}

        for episode, scenes in episode_to_scenes.items():
            episode_graph = nx.DiGraph()
            for scene in scenes:
                for line in scene._script:
                    speaker, text = line
                    if speaker != Tokens.DESCRIPTION_TOKEN:
                        for character in scene._people:
                            if character == speaker:
                                continue
                            self._add_or_update_edge(episode_graph, speaker, character)

            graphs[episode] = episode_graph

        return graphs

    def _create_seasons_graph(self):
        pass

    def _add_or_update_edge(self, graph, origin, destination):
        if graph.has_edge(origin, destination):
            graph[origin][destination]['weight'] += 1
        else:
            graph.add_edge(origin, destination, weight=1)


if __name__ == '__main__':
    episode = '01'
    season = '2'
    graph_creator = GraphCreator(f'parsed/season{season}.pkl')
    graph_creator.export_episode_graph_to_gephi(episode, f'season_{season}_episode_{episode}.gexf')
    graph_creator.pickle_season_graphs(f'pickled_graphs/graphs_season_{season}.pkl')
