import json
import string
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from util.project_path import project_path


@dataclass(frozen=True)
class WordMeaning:
    word: str
    definition: str
    part_of_speech: str | None
    sentence: str | None
    synonyms: list[str] | None


class LexiconSource(Enum):
    WORDSET = 1


class Lexicon(ABC):
    @abstractmethod
    def define(self, word: str) -> list[WordMeaning]:
        pass


class LexiconWordset(Lexicon):
    @staticmethod
    def __get_file_path(first_letter: str) -> Path:
        first_letter = first_letter.lower()

        if len(first_letter) > 1:
            raise ValueError(
                f"Argument 'first_letter' must be single character. Got {first_letter} with length = "
                f"{len(first_letter)}.")

        if first_letter in string.ascii_lowercase:
            file_name = f"{first_letter}.json"
        else:
            file_name = "misc.json"

        # TODO: use project_root / <path> representation
        return project_path(f'datasets/wordset/data/{file_name}')

    @staticmethod
    def __get_dict_for(first_letter: str) -> dict[str, dict[str, str | list[dict[str, str]]]]:
        if len(first_letter) > 1:
            raise ValueError(
                f"Argument 'first_letter' must be single character. Got {first_letter} with length = "
                f"{len(first_letter)}.")

        file_path = LexiconWordset.__get_file_path(first_letter)
        with open(file_path) as f:
            word_dict = json.load(f)

        return word_dict

    @staticmethod
    def __wordset_dict_to_word_meaning_obj(wordset_dict: dict[str, str | list[dict[str, str]]]) -> list[WordMeaning]:
        meanings_list = []

        word = wordset_dict['word']
        for meaning in wordset_dict['meanings']:
            definition = meaning['def']
            part_of_speech = meaning['speech_part'] if 'speech_part' in meaning else None
            synonyms = meaning['synonyms'] if 'synonyms' in meaning else None
            sentence = meaning['example'] if 'example' in meaning else None

            meanings_list.append(WordMeaning(word, definition, part_of_speech, sentence, synonyms))

        return meanings_list

    def define(self, word: str) -> list[WordMeaning] | None:
        letter_dict = LexiconWordset.__get_dict_for(word[0])

        if word not in letter_dict:
            return None
        else:
            return LexiconWordset.__wordset_dict_to_word_meaning_obj(letter_dict[word])


def lexicon_from(dict_source: LexiconSource) -> Lexicon:
    if dict_source == LexiconSource.WORDSET:
        return LexiconWordset()
