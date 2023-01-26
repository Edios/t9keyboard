class TestWordProcessor:
    """
    Test cases:
    1. Check if T9 mode was triggered correctly.
    - Spawn NumpadKeyboard object, change keyboard mode to corresponding one and use on_press_reaction method
    with parameter of KeyCode. Called method will be mocked.

        Pass criteria: Mocked method was called correctly.

    2. Check if SingleTapMode was triggered correctly.
    - Spawn NumpadKeyboard object, change keyboard mode to corresponding one and use on_press_reaction method
    with parameter of KeyCode. Called method will be mocked.

        Pass criteria: Mocked method was called correctly

    """
# TODO: Convert this code sample into unit test
# word_processor = WordProcessor()
#
# word_processor.append_characters("cat")
# queue_value = word_processor.queued_word  # cat
# word_processor.finish_queued_word()
# print(word_processor.get_words())  # cat
#
# characters = ["d", "o", "g"]
# for character in characters:
#     word_processor.append_characters(character)
# word_processor.finish_queued_word()
# print(word_processor.get_last_word())  # dog
#
# print(word_processor.get_words(slicing=slice(1)))  # cat
# print(word_processor.get_words(slicing=slice(2)))  # "cat dog"
# word_processor.clear_word_processor_fields()
# print(word_processor.get_words())  # ""
# x = word_processor.count_last_word_length() # raise exception
