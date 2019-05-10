import os
import pickle
from common import Scene
from common import Tokens
from common import NameUtils
import itertools
import pandas as pd


class ScriptParser(object):
    def __init__(self):
        self._name_resolver = NameUtils()
        self._all_people = set()


    def parse_episode(self, season, episode, file_path):
        with open(file_path, mode='r', encoding="utf-8") as episode_file:
            lines = episode_file.readlines()
            scenes = []
            current_scene = None
            clean_lines = [line.strip() for line in lines]
            filtered_lines = list(filter(lambda line: line != '', clean_lines))

            for line in filtered_lines:
                if self._should_ignore(line):
                    continue
                if self._is_scene_start(line):
                    if current_scene is not None:
                        scenes.append(current_scene)
                    current_scene = Scene(season, episode, line)
                elif self._is_speaking(line):
                    speaker_and_text = self._parse_speaking(line)
                    resolved_speaker_name = self._name_resolver.resolve_name(speaker_and_text[0], season, episode, len(scenes) + 1)
                    current_scene.add_script(resolved_speaker_name, speaker_and_text[1])
                    self._all_people.add(resolved_speaker_name)
                else:
                    current_scene.add_script(Tokens.DESCRIPTION_TOKEN, line)

            scenes.append(current_scene)
            return scenes

    def _should_ignore(self, line):
        ignore_start_words = ['TITLE SEQUENCE', 'CREDITS']
        return any(line.startswith(start_pattern) for start_pattern in ignore_start_words)

    def _is_scene_start(self, line):
        scene_start_words = ['INT.', 'EXT.', 'CUT TO:', 'INT:', 'EXT:']
        return any(line.startswith(start_pattern) for start_pattern in scene_start_words)

    def _is_speaking(self, line):
        return line.find(':') > 0

    def _parse_speaking(self, line):
        return line.split(':', 1)

    def get_all_people(self):
        return self._all_people


def update_people_list(list_of_people):
    pickle_path = 'parsed/people_list.pkl'
    text_path = 'parsed/people_list'
    people = list_of_people
    if os.path.exists(pickle_path):
        with open(pickle_path, mode='rb') as people_list_file:
            people = pickle.load(people_list_file)
            people.update(list_of_people)

    with open(pickle_path, mode='wb') as people_list_file:
        pickle.dump(people, people_list_file)

    with open(text_path, mode='wb') as people_list_file:
        people_list_file.write('\n'.join(people).encode('utf-8'))


def parse_to_df(list_of_Scenes):
    """
        Parse list of Scene objects to DataFrame of this format:
            {"season": 0,
               "episode": 0,
               "scene": 0,
               "place": "",
               "character1": "1",
               "character2": "2",
               "text": "lalala"}
    :return:
    """

    # TODO: Need to clean the names (DESC in the scene._script tuple)
    parsed_data = []

    for index, scene in enumerate(list_of_Scenes):

        names_combinations = list(itertools.combinations(scene._people, 2))
        for comb in names_combinations:
            my_dict = {}
            my_dict["season"] = scene._season
            my_dict["episode"] = scene._episode
            my_dict["scene"] = index
            my_dict["place"] = scene._place
            my_dict["character1"] = comb[0]
            my_dict["character2"] = comb[1]
            my_dict_append = dict(my_dict)
            for tup in scene._script:
                desc, text = tup
                if desc == "DESCRIPTION":
                    continue
                else:
                    my_dict_append = dict(my_dict_append)
                    my_dict_append["text"] = text
                    parsed_data.append(my_dict_append)
    print(parsed_data)
    df = pd.DataFrame(parsed_data)
    df = df[["season", "episode", "scene", "place", "character1", "character2", "text"]]
    return df


if __name__ == '__main__':
    parser = ScriptParser()
    parse_season = '7'

    data_dir = 'data/all'
    files = os.listdir(data_dir)
    filtered_files = filter(lambda file_name: 'bad' not in file_name, files)
    all_scenes = []
    for file in filtered_files:
        season = file.split('_')[0]
        episode = file.split('_')[1][:-4]
        full_file_path = os.path.join(data_dir, file)
        if season == parse_season:
            all_scenes = all_scenes + parser.parse_episode(season, episode, full_file_path)

    with open(f'parsed/season{parse_season}.pkl', mode='wb') as output_file:
        pickle.dump(all_scenes, output_file)

    update_people_list(parser.get_all_people())


    # TODO: Shay's part, think if we need it.
    # # Parse to csv
    # df = parse_to_df(all_scenes)
    # df_name = f"{parse_season}_parsed.csv"
    # df.to_csv(os.path.join("data", "parsed", df_name), index=False)



