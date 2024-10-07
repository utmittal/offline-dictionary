import json
from os import listdir
from pathlib import Path
from string import ascii_lowercase

import pytest

from offlinedictionary.util.project_path import PROJECT_ROOT

WORDSET_DATA_DIRECTORY = PROJECT_ROOT / 'datasets/wordset/data/'
VALID_NAMES = ['misc'] + [_ for _ in ascii_lowercase]


def wordset_data_valid_file_name_generator():
    yield from VALID_NAMES


def wordset_datafile_path_generator():
    yield from WORDSET_DATA_DIRECTORY.glob('*.json')


def wordset_datafile_path_ids(path: Path) -> str:
    return path.absolute().__str__()


def get_all_wordset_data_file_names():
    data_file_names = []
    for file_path in listdir(WORDSET_DATA_DIRECTORY):
        data_file_names.append(Path(file_path).name.split('.')[0])

    return data_file_names


def wordset_top_level_key_generator():
    for file_path in WORDSET_DATA_DIRECTORY.glob('*.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            top_level_dict = json.load(f)

        yield from top_level_dict.keys()


def wordset_key_value_generator():
    for file_path in WORDSET_DATA_DIRECTORY.glob('*.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            top_level_dict = json.load(f)

        for top_level_key in top_level_dict:
            yield top_level_key, top_level_dict[top_level_key]


def wordset_key_value_ids(key_value: tuple[str, dict]) -> str:
    return key_value[0]


@pytest.mark.parametrize('valid_name', wordset_data_valid_file_name_generator())
def test_data_file_exists_for_every_valid_name(valid_name):
    data_file_names = get_all_wordset_data_file_names()

    assert valid_name in data_file_names


@pytest.mark.parametrize('datafile_path', wordset_datafile_path_generator(), ids=wordset_datafile_path_ids)
def test_validate_each_data_file_is_parseable_json(datafile_path):
    with open(datafile_path, 'r', encoding='utf-8') as f:
        json.load(f)  # json will raise its own parsing errors


@pytest.mark.parametrize('datafile_path', wordset_datafile_path_generator(), ids=wordset_datafile_path_ids)
def test_validate_each_data_file_is_a_dictionary_object(datafile_path):
    with open(datafile_path, 'r', encoding='utf-8') as f:
        letter_indexed_dictionary = json.load(f)

    assert isinstance(letter_indexed_dictionary, dict)


@pytest.mark.parametrize("key_value", wordset_key_value_generator(), ids=wordset_key_value_ids)
def test_validate_top_level_words_have_valid_structure(key_value):
    word = key_value[0]
    word_dict = key_value[1]

    # TODO: should these be separate tests?
    assert isinstance(word, str)
    assert isinstance(word_dict, dict)
    # we only care about these two keys
    assert {'word', 'meanings'} <= word_dict.keys()
    for meaning in word_dict['meanings']:
        # in this particular case, we specify all values even though we don't care about id and labels. This is
        # because not every meaning entry has all the values, so we need to reverse our check.
        assert meaning.keys() <= {'id', 'def', 'speech_part', 'example', 'synonyms', 'labels'}
