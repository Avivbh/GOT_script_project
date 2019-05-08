import os
import pickle
from common import Scene
from common import Tokens
from common import NameUtils


class ScriptParser(object):
    def __init__(self):
        self._name_resolver = NameUtils()

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


if __name__ == '__main__':
    parser = ScriptParser()
    parse_season = '3'

    data_dir = '/Users/avivbh/dev/study/nlp/GOT_script_project/data/all'
    files = os.listdir(data_dir)
    filtered_files = filter(lambda file_name: 'bad' not in file_name, files)
    all_scenes = []
    for file in filtered_files:
        season = file.split('_')[0]
        episode = file.split('_')[1][:-4]
        full_file_path = os.path.join(data_dir, file)
        if season == parse_season:
            all_scenes = all_scenes + parser.parse_episode(season, episode, full_file_path)

    with open(f'/Users/avivbh/dev/study/nlp/GOT_script_project/parsed/season{parse_season}.pkl', mode='wb') as output_file:
        pickle.dump(all_scenes, output_file)


