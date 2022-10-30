"""
# from pynput.keyboard import Key, Listener
#
# def on_press(key):
#     print('{0} pressed'.format(
#         key))
#
# def on_release(key):
#     print('{0} release'.format(
#         4862139784key))
#     if key == Key.esc:
#         # Stop listener
#
#         return False
#
# # Collect events until released
# with Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()

#######################Diffrent libary -sucks for debugging
# import keyboard
# import time
# keyboard.start_recording()
# time.sleep(7)
# events = keyboard.stop_recording()
# keyboard.replay(events)




"""
# Counter of pressed key

# import tkinter as tk
#
# root = tk.Tk()
#
#
# def triggered_method(param):
#     print(f"++++++++ {param} ++++++++++++")
#
#
# def key(event):
#     print(repr(event.char), repr(event.keysym), repr(event.keycode))
#     if event.char=="KP_4":
#         triggered_method("KP_4")
# root.bind("<Key>", key)
# root.mainloop()

import tkinter as tk
from tkinter import ttk

"""
/*-7894561230,+

Num_Lock
KP_Divide
KP_Multiply
KP_Subtract
KP_Home
Num_Lock
KP_7
KP_8
KP_9
KP_4
KP_5
KP_6
KP_1
KP_2
KP_3
KP_0
KP_Separator
KP_Enter
KP_Add
Control_L

"""


events_list = []
typed=[]

def trigger_checking_sequence(listChar):
    """
    Determine if its double click
    :param listChar:
    :return:
    """
    print(f"Sequence {'|'.join(listChar)}")

    #Typed is output display
    if listChar[-1] ==listChar[-2]:
        typed.append(listChar[-2])

    if all(x == listChar[0] for x in listChar) and not listChar.__len__()==0:
        print("Its doubleclick")
    else:
        print("Its not doubleclick")


def add_to_event_list(input: str, target: list):
    print(input)
    #target.append(input)
    global events_list
    events_list.append(input)
    trigger_checking_sequence(events_list)
    if target.__len__()>2:
        events_list.clear()


root = tk.Tk()
e = ttk.Entry(root)
e.place(x=1, y=1)
e.bind('<Key>', lambda ev: add_to_event_list(ev.keysym, events_list))
root.mainloop()
