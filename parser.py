import os
import pickle


description_token = 'DESCRIPTION'


def parse_episode(season, episode, file_path):
    with open(file_path, mode='r', encoding="utf-8") as episode_file:
        lines = episode_file.readlines()
        scenes = []
        current_scene = None
        clean_lines = [line.strip() for line in lines]
        filtered_lines = list(filter(lambda line: line != '', clean_lines))

        for line in filtered_lines:
            if should_ignore(line):
                continue
            if is_scene_start(line):
                if current_scene is not None:
                    scenes.append(current_scene)
                current_scene = Scene(season, episode, line)
            elif is_speaking(line):
                speaker_and_text = parse_speaking(line)
                current_scene.add_script(speaker_and_text[0], speaker_and_text[1])
            else:
                current_scene.add_script(description_token, line)

        scenes.append(current_scene)
        return scenes


def should_ignore(line):
    ignore_start_words = ['TITLE SEQUENCE', 'CREDITS']
    return any(line.startswith(start_pattern) for start_pattern in ignore_start_words)


def is_scene_start(line):
    scene_start_words = ['INT.', 'EXT.', 'CUT TO:', 'INT:', 'EXT:']
    return any(line.startswith(start_pattern) for start_pattern in scene_start_words)


def is_speaking(line):
    return line.find(':') > 0


def parse_speaking(line):
    return line.split(':', 1)


class Scene(object):
    def __init__(self, season, episode, place):
        self._season = season
        self._episode = episode
        self._place = place
        self._script = []
        self._people = set()

    def add_script(self, entity, text):
        self._script.append((entity, text))
        if entity != description_token:
            self._people.add(entity)


if __name__ == '__main__':
    parse_season = '2'

    data_dir = '/Users/avivbh/dev/study/nlp/script_project/data/all'
    files = os.listdir(data_dir)
    filtered_files = filter(lambda file_name: 'bad' not in file_name, files)
    all_scenes = []
    for file in filtered_files:
        season = file.split('_')[0]
        episode = file.split('_')[1][:-4]
        full_file_path = os.path.join(data_dir, file)
        if season == parse_season:
            all_scenes = all_scenes + parse_episode(season, episode, full_file_path)

    with open(f'/Users/avivbh/dev/study/nlp/script_project/season{parse_season}.pkl', mode='wb') as output_file:
        pickle.dump(all_scenes, output_file)


