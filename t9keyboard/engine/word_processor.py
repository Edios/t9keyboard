from typing import List


class WordProcessor:
    typed_words: List[str]
    queued_word: str

    def append_characters(self, characters: str):
        """

        :param characters:
        """
        pass

    def finish_word(self):
        pass

    def get_words(self, slicing: slice = slice(0, None)) -> str:
        """

        :param slicing:
        :param all:
        """
        pass

    def get_last_word(self) -> str:
        return self.get_words(slicing=slice(-1, None, None))

    def get_all_words(self) -> str:
        return self.get_words()

    def count_last_word(self, count_additional_space=False) -> int:
        pass

    def clear_typed_words(self):
        pass

    def clear_queued_word(self):
        pass
