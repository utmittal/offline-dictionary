import json
import string
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

from util.project_path import project_path


class LexiconSource(Enum):
    WORDSET = 1


class Lexicon(ABC):
    @abstractmethod
    def define(self, word: str) -> list[str]:
        pass


class LexiconWordset(Lexicon):
    @staticmethod
    def __get_file_path(first_letter: str) -> Path:
        if len(first_letter) > 1:
            raise ValueError(
                f"Argument 'first_letter' must be single character. Got {first_letter} with length = "
                f"{len(first_letter)}.")

        if first_letter in string.ascii_lowercase:
            file_name = f"{first_letter}.json"
        else:
            file_name = "misc.json"

        return project_path(f'datasets/wordset/data/{file_name}')

    @staticmethod
    def __get_dict_for(first_letter: str) -> dict[str, dict[str, str | list]]:
        if len(first_letter) > 1:
            raise ValueError(
                f"Argument 'first_letter' must be single character. Got {first_letter} with length = "
                f"{len(first_letter)}.")

        file_path = LexiconWordset.__get_file_path(first_letter)
        with open(file_path) as f:
            word_dict = json.load(f)

        return word_dict

    def define(self, word: str) -> list[str] | None:
        first_letter = word[0].lower()
        letter_dict = LexiconWordset.__get_dict_for(first_letter)

        if word not in letter_dict:
            return None
        else:
            word_data = letter_dict[word]
            return [meaning['def'] for meaning in word_data['meanings']]


def lexicon_from(dict_source: LexiconSource) -> Lexicon:
    if dict_source == LexiconSource.WORDSET:
        return LexiconWordset()
