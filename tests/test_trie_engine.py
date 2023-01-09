import pytest


class TestTrieEngine:
    """
    Test cases:

    1. Trie inserting
    - Spawn empty Trie object and check if inserting an element works.
        Pass criteria: Number of nodes got increased

    2. Search in trie for full word only
    - Spawn word-preloaded Trie object and see if inserting an element works.
        Pass criteria: Returned list contains only desired word

    3. Search in trie for all word completions
    - Spawn word-preloaded Trie object and see if search for item works.
        Pass criteria: Returned list contains all words started with prefix

    4. Search in trie sort search result in order by weight
    - Spawn word-preloaded Trie object and see if search for item works.
        Pass criteria: Search results are in ordered by word weight.

    5. Search in trie for prefix places full words on the first position
    - Spawn word-preloaded Trie object and see if search for item works.
        Pass criteria: Full word is on the first place of search result

    6. Search in trie returns empty list when it's not matching anything
    - Spawn word-preloaded Trie object and see if search for not existing key
        Pass criteria: Empty dictionary should be returned
    """

    def test_trie_inserting(self, empty_trie):
        """
        Spawn empty Trie object and check if inserting an element works.
        Pass criteria: Number of nodes got increased
        :param empty_trie: pytest fixture of empty Trie object
        """
        nodes_before_inserting = empty_trie.root.children.__len__()
        empty_trie.insert("whey")
        nodes_after_inserting = empty_trie.root.children.__len__()
        assert nodes_before_inserting < nodes_after_inserting

    def test_search_in_trie_for_full_word_only(self, word_preloaded_trie):
        """
        Spawn word-preloaded Trie object and see if inserting an element works.
        Pass criteria: Returned list contains only desired word
        :param word_preloaded_trie: pytest fixture of word preloaded Trie object
        """
        search_result = word_preloaded_trie.search_for_words_starts_with_prefix("what", full_words_only=True)
        assert search_result == [("what", 0)]

    def test_search_in_trie_for_words_started_with_prefix(self, word_preloaded_trie):
        """
        Spawn word-preloaded Trie object and see if search method returns words started with prefix.
        Pass criteria: Returned list contains all words started with prefix
        :param word_preloaded_trie: pytest fixture of word preloaded Trie object
        """
        search_result = word_preloaded_trie.search_for_words_starts_with_prefix("what")
        assert search_result == [('what', 0), [('whats', 0), ('whatever', 0)]]

    def test_trie_search_results_are_sorted_by_weight(self, weighted_word_preloaded_trie):
        """
        Spawn word-preloaded Trie object and see if search returns words sorted by weight.
        Pass criteria: Search results are in ordered by word weight.
        :param weighted_word_preloaded_trie: pytest fixture of word and weight preloaded Trie object
        """
        search_result = weighted_word_preloaded_trie.search_for_words_starts_with_prefix("wha")
        assert search_result == [[('whatever', 4), ('wham', 3), ('whats', 2), ('what', 0)]]

    def test_trie_search_results_first_position_is_full_word(self, weighted_word_preloaded_trie):
        """
        Spawn word-preloaded Trie object and see if search for item put full words in the first place (omitting weight)
        Pass criteria: Full word is on the first place of search result
        :param weighted_word_preloaded_trie: pytest fixture of word and weight preloaded Trie object
        """
        search_result = weighted_word_preloaded_trie.search_for_words_starts_with_prefix("what")
        assert search_result[0] == ('what', 0)

    def test_trie_search_returns_empty_list_when_no_matches(self, weighted_word_preloaded_trie):
        """
        Spawn word-preloaded Trie object and see if search for not existing key returns empty list,
        Pass criteria: Empty dictionary should be returned
        :param weighted_word_preloaded_trie: pytest fixture of word and weight preloaded Trie object
        """
        search_result = weighted_word_preloaded_trie.search_for_words_starts_with_prefix("note")
        assert search_result == list()
