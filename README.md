
# T9 Keyboard controled by Numpad keyboard.

Project of T9 keyboard which is controled by numpad keyboard buttons. 
Application takes sequence of digits, convert it to corresponding letters combos and use Trie tree search to match sequence with potentially words.
When user choose a phrase from available predicted words search results, it will be written to screen. 

## Preview
Using application to type in notepad:

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Instalation guide and system requirements

- To run project this code, you need Python 3.10 + (usage of match/case feature).
- Program runs only on **windows** platform (due to problems on Linux keys signal suppression)

```bash
  cd <main project directory>
  pip install -r requirements.txt
  python run.py

```


## Key bindings
    Default key actions for T9 mode.
        """
        +-------+-------+-------++-------+
        |   7   |   8   |   9   ||   +   |
        |  .?!  |  ABC  |  DEF  ||       |
        +-------+-------+-------+|       |
        |   4   |   5   |   6   || BACK  |
        |  GHI  |  JKL  |  MNO  || SPACE |
        +-------+-------+-------++-------+
        |   1   |   2   |   3   |
        | PQRS  |  TUV  |  WXYZ |
        +-------+-------+-------+
        |       0       |   .   |
        |     SPACE     |SWITCH |
        +-------+-------+-------+
        """
        Digit key 7 :
            - type Dot sign
        Digit keys 8, 9, 4, 6, 7, 1, 2, 3 :
            - Add digit to queue.
        Dot key (Del):
            - switch word hint (phrase)
        Digit key 0 :
            - Accept current hint phrase. Then write phrase as keyboard output
        Plus key + :
            - Backspace

## Running Tests

Pytest is configured to be runned from main project directory.
To run tests, use the following command.

```bash
  cd <main project directory>
  pytest
```

