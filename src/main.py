# library imports
from pynput import keyboard
from pynput.keyboard import Key, Controller
import time
import tkinter as tk
from tkinter import messagebox
import json

# default translations (english to spanish)
translate = {
    "a": "á",
    "e": "é",
    "i": "í",
    "o": "ó",
    "u": "ú",
    "n": "ñ",
    "A": "Á",
    "E": "É",
    "I": "Í",
    "O": "Ó",
    "U": "Ú",
    "N": "Ñ",
    "?": "¿",
    "!": "¡"
}

# laod translations
with open("./translate.json", encoding="utf8") as f:
    translate = json.load(f);

# variable initializaition
# is program running
running = True
keyboard_controller = Controller()

active = False
lastkey = ''
t = 0
threshold = 5

# tkinter
window = tk.Tk()
window.title("Keyboard Translator")
window.resizable(False, False)

# when user exits
def on_closing():
    if messagebox.askokcancel("Exit Application", "Are you sure you want to exit?"):
        running = False
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

# when user presses button
def onButtonPress():
    global translate
    text = translationBox.get("1.0", tk.END)
    text = text.split("\n")
    # analyze the user's translations
    newTranslations = {}
    for txt in text:
        if txt.strip() == "":
            continue
        txtSplit = txt.strip().split(":")
        newTranslations[txtSplit[0]] = txtSplit[1]
    translate = newTranslations
    # saves data
    with open("./translate.json", "w") as tr: 
        json.dump(translate, tr)

# make label to instruct user
instructions = tk.Label(window, text = "Enter your translations. To use your translations, hold the translation key for a bit longer than usual.")

# display all translations
translationBox = tk.Text(window)
for tr in translate:
    translationBox.insert(tk.END, str(tr) + ":" + str(translate[tr]) + "\n")

# create button
button = tk.Button(window, text = "SET TRANSLATIONS", width = 30, command = onButtonPress, bg="#848484", fg="white")

# pack components
instructions.pack(padx=15, pady=15)

translationBox.pack(padx=15, pady=15)
translationBox.focus_set()

button.pack(padx=15, pady=15)

# checks if key is tapped and should be translated
def check(key):
    # fetch global variables
    global active, keyboard_controller, lastkey, t
    # get character that is being typed
    try:
        k = key.char  # single-char keys
        if key.char in translate.values():
            return
    except:
        k = key.name  # other keys
        if key.name == "backspace":
            return
    if k in translate.keys():
        active = True
        lastkey = k
        t = 0
    else:
        active = False
        lastkey = False
        t = 0

# when key is released
def check_release(key):
    # fetch global variables
    global active, keyboard_controller, lastkey, t
    # get character that is being typed
    try:
        k = key.char  # single-char keys
        if key.char in translate.values():
            return
    except:
        k = key.name  # other keys
        if key.name == "backspace":
            return
    # if the key being released is the last key typed...
    if k == lastkey:
        # if the user waited for sufficient time...
        if t >= threshold and active:
            active = False
            lastkey = False
            t = 0
            keyboard_controller.press(Key.backspace)
            keyboard_controller.release(Key.backspace)
            # type new key
            keyboard_controller.type(translate[k])


# key listeners
listener = keyboard.Listener(on_press=check, on_release=check_release, supress=True)
listener.start()

# main loop
def startAll():
    global t
    while running:
        t += 1
        time.sleep(0.05)
        try:
            window.update()
        except:
            break
startAll()
