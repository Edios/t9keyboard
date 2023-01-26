import pytest


class TestNumpadKeyboard:
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

    3. Check if called "handle" method of mode have received correctly mapped key in argument
    - Spawn NumpadKeyboard object, change keyboard mode to corresponding one and use on_press_reaction method
    with parameter of KeyCode. Called method will be mocked.

        Pass criteria: Mocked method have correct data in argument

    4. Check if switching keyboard mode work correctly
    - Spawn NumpadKeyboard object, check value of keyboard_mode, then use method switch_keyboard_mode.

        Pass criteria: Keyboard mode is different from initial value

    5. Check if map_virtual_key_to_known_button returns correctly mapped value.
    - Spawn NumpadKeyboard object, use map_virtual_key_to_known_button with argument which is known VirtualKey Code.

        Pass criteria: Virtual-key code is correctly translated to keypad button value

    6.  Check if map_virtual_key_to_known_button returns exception when unknown vk value was passed.
    - Spawn NumpadKeyboard object, use map_virtual_key_to_known_button with argument which is unknown VirtualKey Code.

        Pass criteria: Method returns exception when Virtual-key code is unknown.
    """

    def test_calling_t9_mode(self, mocker, numpad_keyboard_t9, five_key):
        """
        Check if T9 mode was triggered correctly.
        Spawn NumpadKeyboard object, change keyboard mode to corresponding one and use on_press_reaction method
        with parameter of KeyCode. Called method will be mocked.
        Pass criteria: Mocked method was called correctly.

        :param mocker: Mock of handle method in child object
        :param numpad_keyboard_t9: NumpadKeyboard object with t9 mode
        :param five_key: pytest fixture of answer
        """
        t9 = mocker.patch("t9keyboard.t9_mode.T9Mode.handle_t9_mode")
        numpad_keyboard_t9.on_press_reaction(five_key[0])
        assert t9.call_count == 1

    def test_calling_single_tap_mode(self, mocker, numpad_keyboard_single_tap, five_key):
        """
        Check if Single Tap mode was triggered correctly.
        Spawn NumpadKeyboard object, change keyboard mode to corresponding one and use on_press_reaction method
        with parameter of KeyCode. Called method will be mocked.
        Pass criteria: Mocked method was called correctly.

        :param mocker: Mock of handle method in child object
        :param numpad_keyboard_single_tap: NumpadKeyboard object with SingleTapMode
        :param five_key: pytest fixture of answer
        """
        single_tap = mocker.patch("t9keyboard.single_tap_keyboard_mode.SingleTapMode.handle_single_tap_mode")
        numpad_keyboard_single_tap.on_press_reaction(five_key[0])
        assert single_tap.call_count == 1

    # TODO: This test is corelated with T9Mode.map_key()
    def test_handle_mode_recived_correctly_mapped_key(self, mocker, numpad_keyboard_t9, five_key):
        """
        Check if T9 mode parameter
        Spawn NumpadKeyboard object, change keyboard mode to corresponding one and use on_press_reaction method
        with parameter of KeyCode. Called method will be mocked.
        Pass criteria: Called "handle" method of mode have received correctly mapped key in argument

        :param mocker: Mock of handle method in child object
        :param numpad_keyboard_t9: NumpadKeyboard object with t9 mode
        :param five_key: pytest fixture of answer
        """
        t9 = mocker.patch("t9keyboard.t9_mode.T9Mode.handle_t9_mode")
        numpad_keyboard_t9.on_press_reaction(five_key[0])
        assert t9.call_args.args[0] == five_key[1]

    def test_switch_keyboard_mode_method(self, numpad_keyboard_t9):
        """
        Spawn NumpadKeyboard object, check value of keyboard_mode, then use method switch_keyboard_mode.
        Pass criteria: Keyboard mode is different from initial value
        :param numpad_keyboard_t9: NumpadKeyboard object with t9 mode
        """
        initial_keyboard_mode = numpad_keyboard_t9.keyboard_mode
        numpad_keyboard_t9.switch_keyboard_mode()
        assert initial_keyboard_mode != numpad_keyboard_t9.keyboard_mode

    def test_virtual_key_mapping_method_returns_correctly_mapped_keypad_button(self, numpad_keyboard, five_key):
        """
        Spawn NumpadKeyboard object, use map_virtual_key_to_known_button with argument which is known VirtualKey Code.
        Pass criteria: Virtual-key code is correctly translated to keypad button value
        :param numpad_keyboard: NumpadKeyboard object with t9 mode
        :param five_key: pytest fixture of answer
        """
        maped_value = numpad_keyboard.map_virtual_key_to_known_button(five_key[0].vk)
        assert maped_value == five_key[1].keypad_button

    def test_virtual_key_mapping_method_returns_exception_when_unknown_value_was_passed(self, numpad_keyboard):
        """
        Spawn NumpadKeyboard object, use map_virtual_key_to_known_button with argument which is known VirtualKey Code.
        Pass criteria: Method returns exception when Virtual-key code is unknown.
        :param numpad_keyboard: NumpadKeyboard object with t9 mode
        :param five_key: pytest fixture of answer
        """
        with pytest.raises(Exception):
            numpad_keyboard.map_virtual_key_to_known_button("999")