import pickle
import re
from textblob import TextBlob

import networkx as nx
from collections import defaultdict
from common import Tokens


class GraphCreator(object):
    def __init__(self, scenes_file_path):
        self._scenes = self._open_scenes(scenes_file_path)
        self._create_episodes_graphs()
        self._episodes_graphs = self._create_episodes_graphs()
        self._season_graph = self.get_full_season_graph()

    def export_episode_graph_to_gephi(self, episode, file_path):
        nx.write_gexf(self._episodes_graphs[episode], file_path)

    def export_season_graph_to_gephi(self, file_path):
        nx.write_gexf(self._season_graph, file_path)

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
                            # self._add_or_update_edge(episode_graph, speaker, character)
                            self._add_or_update_edge(episode_graph, speaker, character, text)

            # Normalize sentiment
            weights = nx.get_edge_attributes(episode_graph, 'weight')
            likes = nx.get_edge_attributes(episode_graph, 'like')
            for e in episode_graph.edges:
                likes[e] = likes[e]/weights[e]
            nx.set_edge_attributes(episode_graph, likes, 'like')
            graphs[episode] = episode_graph

        return graphs

    def get_full_season_graph(self):

        # TODO: Normalize sum of edges over all the graphs

        graphs_li = self._episodes_graphs.values()
        season_graph = nx.DiGraph()
        for graph in graphs_li:
            season_graph.add_edges_from(graph.edges(data=True))
            season_graph.add_nodes_from(graph.nodes(data=True))
        return season_graph

    def _add_or_update_edge(self, graph, origin, destination, text):

        sentiment_polarity = self.get_similarity(text)

        if graph.has_edge(origin, destination):
            graph[origin][destination]['weight'] += 1
            graph[origin][destination]['like'] += sentiment_polarity
        else:
            graph.add_edge(origin, destination, weight=1, like=sentiment_polarity)

    def get_similarity(self, text):
        # Parse line
        REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
        REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

        def preprocess_lines(line):
            new_line = REPLACE_NO_SPACE.sub("", str(line).lower())
            new_line = REPLACE_WITH_SPACE.sub(" ", str(new_line))
            return new_line

        new_line = preprocess_lines(text)
        sentiment_polarity, sentiment_subjectivity = TextBlob(new_line).sentiment
        return sentiment_polarity


if __name__ == '__main__':
    # episode = '01'
    # season = '2'
    # graph_creator = GraphCreator(f'parsed/season{season}.pkl')
    # # graph_creator.export_episode_graph_to_gephi(episode, f'season_{season}_episode_{episode}_sentiment.gexf')
    # graph_creator.export_season_graph_to_gephi(f'season_{season}_sentiment.gexf')
    # graph_creator.pickle_season_graphs(f'pickled_graphs/graphs_season_{season}.pkl')


    for i in range(2,8):
        print("Season: ", i)
        season = str(i)
        graph_creator = GraphCreator(f'parsed/season{season}.pkl')
        # graph_creator.export_episode_graph_to_gephi(episode, f'season_{season}_episode_{episode}_sentiment.gexf')
        graph_creator.export_season_graph_to_gephi(f'season_{season}_sentiment.gexf')
        graph_creator.pickle_season_graphs(f'pickled_graphs/graphs_season_{season}.pkl')
