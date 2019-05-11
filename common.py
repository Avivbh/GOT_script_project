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
        self._name_alias = {
            'eddison': 'eddison tollett',
            'dolorous edd': 'eddison tollett',
            'edd': 'eddison tollett',
            'jon': 'jon snow',
            'the hound': 'hound',
            'rickard': 'rickard karstark',
            'lord karstark': 'rickard karstark',
            'glover': 'robett glover',
            'olenna': 'lady olenna',
            'daario': 'daario naharis',
            'daaerio': 'daario naharis',
            'darrio': 'daario naharis',
            'dario': 'daario naharis',
            'mace': 'mace tyrell',
            'barristan': 'barristan selmy',
            'janos': 'janos slynt',
            'janos slunt': 'janos slynt',
            'danerys': 'daenerys targaryen',
            'danaerys': 'daenerys targaryen',
            'daerneys': 'daenerys targaryen',
            'daeynerys': 'daenerys targaryen',
            'denerys': 'daenerys targaryen',
            'daenerys': 'daenerys targaryen',
            'hizdahr': 'hizdahr zo loraq',
            'aemon': 'maester aemon',
            'lancel': 'lancel lannister',
            'tanner': 'karl tanner',
            'john': 'john royce',
            'alliser': 'alliser thorne',
            'wolkan': 'maester wolkan',
            'meryn': 'meryn trant',
            'young lyanna': 'lyanna mormont',
            'lyanna': 'lyanna mormont',
            'high septon': 'high sparrow',
            'kevan': 'kevan lannister',
            'roose': 'roose bolton',
            'quaithe': 'quaith',
            'rodrik': 'ser rodrik',
            'pycelle': 'maester pycelle',
            'walder': 'walder frey',
            'lollys': 'lollys stokeworth',
            'kraznys': 'kraznys mo nakloz',
            'walda': 'lady walda',
            'ersei': 'cersei',
            'mountian': 'mountain',
            'brinenne': 'brienne',
            'ramsey': 'ramsay',
            'ahsh': 'osha',
            'radzai mo eraz': 'radzal mo eraz',
            'rikon': 'rickon',
            'ahsa': 'osha',
            'tyron': 'tyrion',
            'greyworm': 'grey worm',
            'samwell': 'sam',
        }
        self._names_to_unique = ['man', "ironborn", 'crowd', 'gold cloak', 'announcer', 'lord', 'watchman', 'the group',
                                 'blacksmith' 'woman #9', 'woman', 'tailor', 'woman #8', 'driver', 'frey soldier #3',
                                 'soldier #2', 'soldier #3', 'guard #2', 'soldier #1', 'soldier', 'woman #6', 'baby',
                                 'frey soldier', 'woman #6', 'lord of bones', 'woman #7', 'all', 'girl', 'whore',
                                 'daughter', 'unsullied', 'men', 'messenger', 'mar #2', 'archers', 'wounded soldier',
                                 'musician', 'woman #9', 'farmer hamlet', 'frey soldier #2', 'man #6', 'woman #5',
                                 'bolton guard', 'servant', 'waitress', 'bolton bannerman', 'woman', 'militant',
                                 'cuard #2', 'man #3', 'champion', 'dornish lord', 'meereen slave', 'protester',
                                 'man #4', 'attendant', 'dothraki matron', 'khal #1', 'head prostitute',
                                 'blonde prostitute', 'women', 'dying man', 'maester', 'maester 1', 'bystanders',
                                 'giant', 'soldier #4', 'rider', 'slaver', 'wife#1', 'knight', 'man #2', 'guard #3',
                                 'night’s watchman', 'master', 'priestess', 'brother', 'handmaiden', 'innkeeper',
                                 'knight #2', 'winterfell shepherd', 'priest', 'man #2', 'lhazareen woman', 'client',
                                 'innkeeper\'s daugher', 'frey man', 'prisoner #2', 'knight 1', 'guard 2', 'owner',
                                 'unsullied #1', 'septa', 'whore #1', 'hunters', 'mistress', 'bolton officer',
                                 'first mate', 'young man #2', 'wife #1', 'night’s watchman #1', 'king’s soldier',
                                 'ranger', 'nan', 'guard captain', 'wildling', 'whore #2', 'knight #3', 'leader',
                                 'young man', 'bloodrider #4', 'bloodrider #1', 'bloodrider', 'woman #3', 'brothers',
                                 'boy', 'dothraki woman', 'brothel keeper', 'maester 2', 'man #1', 'male voice #1',
                                 'child of the forest', 'rider', 'guard captain', 'khal #4', 'guard', 'soldier 2']

    def resolve_name(self, name, season, episode, scene_number):
        lower_case_name = name.lower()
        brackets_location = lower_case_name.find('(')
        clean_name = lower_case_name[:brackets_location] if brackets_location > 0 else lower_case_name
        clean_name = clean_name.strip()
        if clean_name in self._names_to_unique:
            return f'{clean_name}{season}{episode}{scene_number} -uq'
        elif clean_name in self._name_alias:
            return self._name_alias[clean_name]
        else:
            return clean_name
