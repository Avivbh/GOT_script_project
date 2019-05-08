class Tokens(object):
    DESCRIPTION_TOKEN = 'DESCRIPTION'


class Scene(object):
    def __init__(self, season, episode, place):
        self._season = season
        self._episode = episode
        self._place = place
        self._script = []
        self._people = set()

    def add_script(self, entity, text):
        self._script.append((entity, text))
        if entity != Tokens.DESCRIPTION_TOKEN:
            self._people.add(entity)


class NameUtils(object):
    def __init__(self):
        self._name_alias = {}
        self._names_to_unique = ['man', "ironborn", 'crowd' 'gold cloak']

    def resolve_name(self, name, season, episode, scene_number):
        lower_case_name = name.lower()
        if lower_case_name in self._names_to_unique:
            return f'{lower_case_name}{season}{episode}{scene_number} - unique'
        elif lower_case_name in self._name_alias:
            return self._name_alias[lower_case_name]
        else:
            return lower_case_name
