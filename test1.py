import cv2
from PIL import ImageGrab
import win32gui
import tkinter as tk
from tkinter.ttk import Combobox
import numpy as np
import pyautogui
import time
import random


def get_window_info():
    def callback(hwnd, window_info):
        if win32gui.IsWindowVisible(hwnd):
            window_info[win32gui.GetWindowText(hwnd)] = hwnd

    window_info = {}
    win32gui.EnumWindows(callback, window_info)
    return window_info


class PokerBot:

    def __init__(self):
        self.root = tk.Tk()
        self.combo = Combobox(self.root, width=120)
        self.window_info = get_window_info()
        self.white = np.array([255, 255, 255])
        self.ranks = {
            '2': cv2.imread('ranks\\2.png', 0),
            '3': cv2.imread('ranks\\3.png', 0),
            '4': cv2.imread('ranks\\4.png', 0),
            '5': cv2.imread('ranks\\5.png', 0),
            '6': cv2.imread('ranks\\6.png', 0),
            '7': cv2.imread('ranks\\7.png', 0),
            '8': cv2.imread('ranks\\8.png', 0),
            '9': cv2.imread('ranks\\9.png', 0),
            'T': cv2.imread('ranks\\T.png', 0),
            'J': cv2.imread('ranks\\J.png', 0),
            'Q': cv2.imread('ranks\\Q.png', 0),
            'K': cv2.imread('ranks\\K.png', 0),
            'A': cv2.imread('ranks\\A.png', 0),
        }

        self.suits = {
            'h': np.array([163, 21, 21]),
            's': np.array([0, 142, 80]),
            'c': np.array([0, 0, 0]),
            'd': np.array([35, 89, 189]),
        }
        self.check_stack = [0]
        self.betting_imgs = {
            '0': cv2.imread('betting\\0.png', 0),
            '1': cv2.imread('betting\\1.png', 0),
            '2': cv2.imread('betting\\2.png', 0),
            '3': cv2.imread('betting\\3.png', 0),
            '4': cv2.imread('betting\\4.png', 0),
            '5': cv2.imread('betting\\5.png', 0),
            '6': cv2.imread('betting\\6.png', 0),
            '7': cv2.imread('betting\\7.png', 0),
            '8': cv2.imread('betting\\8.png', 0),
            '9': cv2.imread('betting\\9.png', 0),
            '.': cv2.imread('betting\\,.png', 0),
        }
        self.betting_coords =[]
    def run(self):
        btn = tk.Button(self.root, text='Ok', command=lambda: self.poker_window())
        keys = []
        for key in get_window_info():
            keys.append(key)
        self.combo['values'] = keys
        self.combo.pack(side='left')
        btn.pack(side='left')
        self.root.mainloop()

    def poker_window(self):
        wind = self.window_info[self.combo.get()]
        win32gui.MoveWindow(wind, 0, 0, 1280, 720, True)
        win32gui.SetForegroundWindow(wind)
        count_screen = 0
        coord_hero_bet = [413, 429, 452, 566]
        while True:
            rect = win32gui.GetWindowRect(wind)
            screen = ImageGrab.grab((rect[0], rect[1], rect[2], rect[3]))
            screen_color = np.array(screen)
            # преобразование в чб
            screen_bw = np.array(screen.convert('L'))  # серый
            screen_bw[screen_bw < 200] = 0  # чёрный
            screen_bw[screen_bw >= 200] = 255  # белый
            hero_bet =screen_bw[coord_hero_bet[0]:coord_hero_bet[1], coord_hero_bet[2]:coord_hero_bet[3]]
            contours, hierarchy = cv2.findContours(hero_bet, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            symbols_hero_bet = []
            for i, contour in enumerate(contours):
                x, y, w, h = cv2.boundingRect(contour)
                if hierarchy[0][i][3] == -1:
                    # cv2.rectangle(hero_chip, (x, y), (x + w, y + h), (100, 0, 0), 1)
                    symbols_hero_bet.append([hero_bet[y:y + h, x:x + w], x])
            symbols_hero_bet = sorted(symbols_hero_bet, key=lambda sym: sym[1])
            list_stack = []
            for symbol in symbols_hero_bet:
                accuracy = [[key, np.sum(symbol[0] == stack) / stack.size] for key, stack in self.betting_imgs.items()
                            if stack.size == symbol[0].size]
                accuracy_key = [i[0] for i in accuracy]
                accuracy_value = [i[1] for i in accuracy]
                if accuracy_value:
                    if max(accuracy_value) > 0.99:
                        list_stack.append(accuracy_key[accuracy_value.index(max(accuracy_value))])
            stack = ''.join(list_stack)
            print(stack)
            cv2.imshow("screen", screen_bw)
            if cv2.waitKey(1) == ord('w'):
                count_screen += 1
                # h1 = str(count_screen) + '1.png'
                # h2 = str(count_screen) + '2.png'
                scr = str(count_screen) + 'screen.png'
                print(scr)
                for i in range(0, len(symbols_hero_bet)):
                    cv2.imwrite(str(i) + str(count_screen) + '.png', symbols_hero_bet[i][0])
                    print(str(i) + str(count_screen) + '.png')
                cv2.imwrite(scr, screen_bw)

PokerBot().run()