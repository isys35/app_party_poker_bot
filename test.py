#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

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
        fastpoker = FastPoker(wind)
        while True:
            rect = win32gui.GetWindowRect(wind)
            screen = ImageGrab.grab((rect[0], rect[1], rect[2], rect[3]))
            screen_color = np.array(screen)
            # преобразование в чб
            screen_bw = np.array(screen.convert('L'))  # серый
            screen_bw[screen_bw < 128] = 0  # чёрный
            screen_bw[screen_bw >= 128] = 255  # белый
            card1_rank_np = screen_bw[442:468, 455:485]
            card2_rank_np = screen_bw[442:468, 526:556]
            card1_suit_np = screen_color[454, 490]
            card2_suit_np = screen_color[454, 562]
            screen_stack_bw = np.array(screen.convert('L'))
            screen_stack_bw[screen_stack_bw < 128] = 0
            screen_stack_bw[screen_stack_bw >= 128] = 255
            # seat0 = screen_stack_bw[392:392 + 20, 15:15 + 130]
            # seat1 = screen_stack_bw[179:179 + 20, 15:15 + 130]
            # seat2 = screen_stack_bw[94:94 + 20, 415:415 + 130]
            # img = screen_stack_bw[527:527+20, 471:471 + 131]
            # contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            # symbols_hero = []
            # for i, contour in enumerate(contours):
            #     x, y, w, h = cv2.boundingRect(contour)
            #     if hierarchy[0][i][3] == -1:
            #         # cv2.rectangle(hero_chip, (x, y), (x + w, y + h), (100, 0, 0), 1)
            #         symbols_hero.append([img[y:y + h, x:x + w], x])
            # symbols_hero = sorted(symbols_hero, key=lambda sym: sym[1])
            # cv2.imshow("screen", screen_stack_bw)
            card1_rank = self.get_rank(card1_rank_np)
            card2_rank = self.get_rank(card2_rank_np)
            card1_suit = self.get_suit(card1_suit_np)
            card2_suit = self.get_suit(card2_suit_np)
            btn_chip = [screen_color[366, 774, 0], screen_color[207, 751, 0], screen_color[162, 402, 0],
                        screen_color[207, 265, 0], screen_color[366, 246, 0], screen_color[455, 626, 0]]
            if card1_rank and card2_rank and 231 in btn_chip:
                check_info = card1_rank + card2_rank + card1_suit + card2_suit + str(btn_chip.index(231))
                if self.check_stack[-1] != check_info:
                    self.check_stack.append(check_info)
                    self.check_stack.pop(-2)
                    hero_cards = [Card(card1_rank, card1_suit), Card(card2_rank, card2_suit)]
                    fastpoker.hands.append({'hero cards': hero_cards, 'btn chip': int(btn_chip.index(231))})
                    fastpoker.run_hand()
            if cv2.waitKey(1) == ord('w'):
                count_screen += 1
                # h1 = str(count_screen) + '1.png'
                # h2 = str(count_screen) + '2.png'
                scr = str(count_screen) + 'screen.png'
                cv2.imwrite(scr, screen_stack_bw)
                cv2.imwrite(str(count_screen) + '0.png', seat0)
                cv2.imwrite(str(count_screen) + '1.png', seat1)
                cv2.imwrite(str(count_screen) + '2.png', seat1)
                # for i in range(0, len(symbols_hero)):
                #     cv2.imwrite(str(i) + '.png', symbols_hero[i][0])
                # cv2.imwrite(scr, hero_chip)
                # print(h1)
                # print(h2)

    def get_rank(self, card):
        """
        получение карты из масссива
        :param card: массив numpy
        :return: string rank
        """
        card_ranks = [rank for rank in self.ranks]
        accuracy = [np.sum(value == card) / card.size for key, value in self.ranks.items()]
        if max(accuracy) > 0.9:
            rank = card_ranks[accuracy.index(max(accuracy))]
            return rank

    def get_suit(self, card):
        """
        получение масти из точки на экране
        :param card: [R G B]
        :return: string suit
        """
        for suit, items in self.suits.items():
            if np.all(card == items):
                return suit


class Opp:
    coords_stack = [[419, 20, 23, 131], [206, 20, 23, 131], [121, 20, 422, 131],
                    [206, 20, 866, 131], [419, 20, 866, 131], [527, 20, 471, 131]]
    action_info = [[392, 20, 15, 130], [179, 20, 15, 130], [94, 20, 414, 130],
                   [179, 20, 863, 130], [392, 20, 863, 130]]
    coords_betting = [[396, 16, 239, 114], [266, 16, 169, 114], [177, 16, 499, 114],
                      [266, 16, 731, 114], [396, 16, 668, 114], [413, 16, 452, 114]]
    pixel_fold = [[385, 96], [172, 96], [87, 495], [172, 918], [385, 918]]
    stack_string = {
        '0': cv2.imread('stack\\0.png', 0),
        '1': cv2.imread('stack\\1.png', 0),
        '2': cv2.imread('stack\\2.png', 0),
        '3': cv2.imread('stack\\3.png', 0),
        '4': cv2.imread('stack\\4.png', 0),
        '5': cv2.imread('stack\\5.png', 0),
        '6': cv2.imread('stack\\6.png', 0),
        '7': cv2.imread('stack\\7.png', 0),
        '8': cv2.imread('stack\\8.png', 0),
        '9': cv2.imread('stack\\9.png', 0),
        'B': cv2.imread('stack\\B.png', 0),
        '.': cv2.imread('stack\\,.png', 0),
    }
    action_string = {
        'call': cv2.imread('action\\call.png', 0),
        'fold': cv2.imread('action\\fold.png', 0),
        'raise': cv2.imread('action\\raise.png', 0),
    }

    streets = ['preflop', 'flop', 'turn', 'river']
    betting_imgs = {
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
    def __init__(self, position):
        self.position = position
        self.street = 'preflop'
        self.seat = None
        self.stack = 0
        self.in_play = True
        self.size_bet = 0
        self.action = {street: [] for street in self.streets}

    def update_stack(self, window):
        coord = self.coords_stack[self.seat]
        rect = win32gui.GetWindowRect(window)
        screen = ImageGrab.grab((rect[0], rect[1], rect[2], rect[3]))
        screen_stack_bw = np.array(screen.convert('L'))
        screen_stack_bw[screen_stack_bw < 170] = 0
        screen_stack_bw[screen_stack_bw >= 170] = 255
        img = screen_stack_bw[coord[0]:coord[0] + coord[1], coord[2]:coord[2] + coord[3]]
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        symbols_hero = []
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            if hierarchy[0][i][3] == -1:
                # cv2.rectangle(hero_chip, (x, y), (x + w, y + h), (100, 0, 0), 1)
                symbols_hero.append([img[y:y + h, x:x + w], x])
        symbols_hero = sorted(symbols_hero, key=lambda sym: sym[1])
        list_stack = []
        for symbol in symbols_hero:
            accuracy = [[key, np.sum(symbol[0] == stack) / stack.size] for key, stack in self.stack_string.items()
                        if stack.size == symbol[0].size]
            accuracy_key = [i[0] for i in accuracy]
            accuracy_value = [i[1] for i in accuracy]
            if accuracy_value:
                if max(accuracy_value) > 0.99:
                    list_stack.append(accuracy_key[accuracy_value.index(max(accuracy_value))])
        stack = ''.join(list_stack)
        stack = stack.replace('B', '')
        try:
            self.stack = float(stack)
        except ValueError:
            self.stack = 0

    def check_action(self, window, players):
        if self.position == 'sb' and len(self.action[self.street]) == 0:
            self.action[self.street].append('SB')
            self.size_bet = 0.5
            print(self.position + ' Поставил малый блайнд ' + str(self.size_bet))
        elif self.position == 'bb' and len(self.action[self.street]) == 0:
            self.action[self.street].append('BB')
            self.size_bet = 1
            print(self.position + ' Поставил большой блайнд ' + str(self.size_bet))
        else:
            print(self.position + ' Ожидаем действия....')
            coord = self.coords_betting[self.seat]
            count = 0
            while True:
                rect = win32gui.GetWindowRect(window)
                screen = ImageGrab.grab((rect[0], rect[1], rect[2], rect[3]))
                screen_stack_bw = np.array(screen.convert('L'))
                screen_stack_bw[screen_stack_bw < 200] = 0
                screen_stack_bw[screen_stack_bw >= 200] = 255
                img = screen_stack_bw[coord[0]:coord[0] + coord[1], coord[2]:coord[2] + coord[3]]
                # cv2.imwrite(str(self.seat)+str(count) + '.png', screen_stack_bw)
                contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                symbols_bet = []
                for i, contour in enumerate(contours):
                    x, y, w, h = cv2.boundingRect(contour)
                    if hierarchy[0][i][3] == -1:
                        # cv2.rectangle(hero_chip, (x, y), (x + w, y + h), (100, 0, 0), 1)
                        symbols_bet.append([img[y:y + h, x:x + w], x])
                symbols_hero_bet = sorted(symbols_bet, key=lambda sym: sym[1])
                list_stack = []
                for symbol in symbols_hero_bet:
                    accuracy = [[key, np.sum(symbol[0] == stack) / stack.size] for key, stack in
                                self.betting_imgs.items()
                                if stack.size == symbol[0].size]
                    accuracy_key = [i[0] for i in accuracy]
                    accuracy_value = [i[1] for i in accuracy]
                    if accuracy_value:
                        if max(accuracy_value) > 0.99:
                            list_stack.append(accuracy_key[accuracy_value.index(max(accuracy_value))])
                size_bet = ''.join(list_stack)
                try:
                    size_bet = float(size_bet)
                except ValueError:
                    size_bet = 0
                max_bet = max([player.size_bet for player in players])
                if size_bet == max_bet and self.position != 'bb':
                    action = 'call'
                    self.call(window, size_bet)
                    return action
                if size_bet == max_bet and self.position == 'bb' and size_bet > 1:
                    action = 'call'
                    self.call(window, size_bet)
                    return action
                if size_bet > max_bet:
                    action = 'raise'
                    self.bet(window, size_bet)
                    return action
                if screen_stack_bw[self.pixel_fold[self.seat][0], self.pixel_fold[self.seat][1]] == 0:
                    action = 'fold'
                    self.in_play = False
                    self.action[self.street].append('F')
                    print(self.position + ' ' + action)
                    return action
                r = len(self.action[self.street])
                if r > 0:
                    if size_bet == 0:
                        action = 'call'
                        self.call(window, max_bet)
                        return action
                # if size_bet == 0:
                #     action = 'call'
                #     self.action[self.street].append('X')
                #     print(self.position + ' чек')
                #     return action
                # if max(accuracy) > 0.99:
                #     action = actions[accuracy.index(max(accuracy))]
                #     if action == 'fold':
                #         self.in_play = False
                #         self.action[self.street].append('F')
                #         print(self.position + ' ' + action)
                #     elif action == 'raise':
                #         self.bet(window, 0)
                #     elif action == 'call':
                #         for_call = max([p.size_bet for p in players]) - self.size_bet
                #         self.call(window, for_call)
                #     return action

    def call(self, window, for_call):
        self.action[self.street].append('C')
        self.size_bet = for_call
        print(self.position + ' колл ' + str(self.size_bet))

    def bet(self, window, bb):
        self.action[self.street].append('R')
        self.size_bet = bb
        print(self.position + ' повысил на ' + str(bb))


class Hero(Opp):
    card_value = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }

    cards_or = {'ep': ['AA', 'AKs', 'AQs', 'AJs', 'ATs', 'AKo',
                       'KK', 'KQs', 'KJs', 'AQo', 'KQo', 'QQ',
                       'QJs', 'AJo', 'JJ', 'TT', '99', '88', '77', '66'],
                'mp': ['AA', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'AKo',
                       'KK', 'KQs', 'KJs', 'KTs', 'AQo', 'KQo', 'QQ', 'QJs',
                       'QTs', 'AJo', 'KJo', 'QJo', 'JJ', 'JTs', 'ATo', 'TT',
                       'T9s', '99', '98s', '88', '87s', '77', '66', '55', '44', '33', '22'],
                'co': ['AA', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s'
                    , 'A4s', 'A3s', 'A2s', 'AKo', 'KK', 'KQs', 'KJs', 'KTs', 'K9s', 'K8s',
                       'AQo', 'KQo', 'QQ', 'QJs', 'QTs', 'Q9s', 'AJo', 'KJo', 'QJo', 'JJ', 'JTs',
                       'J9s', 'ATo', 'KTo', 'QTo', 'JTo', 'TT', 'T9s', 'T8s', 'A9o', '99', '98s',
                       '97s', '88', '87s', '77', '76s', '66', '65s', '55', '54s', '44', '33', '22'],
                'btn': ['AA', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s',
                        'A3s', 'A2s', 'AKo', 'KK', 'KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s',
                        'K5s', 'K4s', 'K3s', 'K2s', 'AQo', 'KQo', 'QQ', 'QJs', 'QTs', 'Q9s', 'Q8s',
                        'Q7s', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s', 'AJo', 'KJo', 'QJo', 'JJ', 'JTs',
                        'J9s', 'J8s', 'J7s', 'ATo', 'KTo', 'QTo', 'JTo', 'TT', 'T9s', 'T8s', 'T7s',
                        'A9o', 'K9o', 'Q9o', 'J9o', 'T9o', '99', '98s', '97s', '96s', 'A8o', 'K8o',
                        '88', '87s', '86s', 'A7o', '77', '76s', '75s', 'A6o', '66', '65s', '64s',
                        'A5o', '55', '54s', 'A4o', '44', 'A3o', '33', 'A2o', '22'],
                'sb': ['AA', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s',
                       'A3s', 'A2s', 'AKo', 'KK', 'KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s',
                       'K5s', 'K4s', 'K3s', 'K2s', 'AQo', 'KQo', 'QQ', 'QJs', 'QTs', 'Q9s', 'Q8s',
                       'Q7s', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s', 'AJo', 'KJo', 'QJo', 'JJ', 'JTs',
                       'J9s', 'J8s', 'J7s', 'ATo', 'KTo', 'QTo', 'JTo', 'TT', 'T9s', 'T8s', 'T7s',
                       'A9o', 'K9o', 'Q9o', 'J9o', 'T9o', '99', '98s', '97s', '96s', 'A8o', 'K8o',
                       'Q8o', '98o', '88', '87s', '86s', 'A7o', 'K7o', '87o', '77', '76s', '75s',
                       'A6o', 'K6o', '66', '65s', '64s', 'A5o', 'K5o', '55', '54s', 'A4o', '44',
                       'A3o', '33', 'A2o', '22'],
                'bb': []
                }
    cards_cold_call = {
        'ep': ['JJ', 'TT', '99', '88', '77', '66', '55'],
        'mp': ['JJ', 'TT', '99', '88', '77', '66', '55', '44'],
        'co': ['99', '88', '77', '66', '55', '44', '33', '22'],
        'btn': ['99', '88', '77', '66', '55', '44', '33', '22'],
        'sb': ['99', '88', '77', '66', '55', '44', '33', '22'],
        'bb': ['99', '88', '77', '66', '55', '44', '33', '22'],
    }
    cards_izolate = {
        'ep': [],
        'mp': ['AA', 'AKs', 'AQs', 'AJs', 'AKo', 'KK', 'KQs', 'KJs', 'AQo', 'KQo', 'QQ', 'QJs',
               'AJo', 'KJo', 'QJo', 'JJ', 'TT', '99', '88', '77', '66'],
        'co': ['AA', 'AKs', 'AQs', 'AJs', 'AKo', 'KK', 'KQs', 'KJs', 'AQo', 'KQo', 'QQ', 'QJs',
               'AJo', 'KJo', 'QJo', 'JJ', 'TT', '99', '88', '77', '66'],
        'btn': ['AA', 'AKs', 'AQs', 'AJs', 'AKo', 'KK', 'KQs', 'KJs', 'AQo', 'KQo', 'QQ', 'QJs',
                'AJo', 'KJo', 'QJo', 'JJ', 'TT', '99', '88', '77', '66'],
        'sb': ['AA', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'AKo', 'KK', 'KQs',
               'KJs', 'KTs', 'AQo', 'KQo', 'QQ', 'QJs', 'QTs', 'AJo', 'KJo', 'QJo', 'JJ', 'JTs',
               'ATo', 'KTo', 'QTo', 'JTo', 'TT', 'A9o', '99', '88', '77', '66'],
        'bb': ['AA', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s',
               'A2s', 'AKo', 'KK', 'KQs', 'KJs', 'KTs', 'K9s', 'AQo', 'KQo', 'QQ', 'QJs', 'QTs',
               'Q9s', 'AJo', 'KJo', 'QJo', 'JJ', 'JTs', 'ATo', 'KTo', 'QTo', 'JTo', 'TT', 'A9o',
               '99', '88', '77', '66']
    }
    cards_3bet = {
        'ep': [['AA', 'AKs', 'AKo', 'KK', 'QQ'],
               ['AA', 'AKs', 'AKo', 'KK', 'QQ', 'AQs', 'AJs', 'AQo', 'KQs']],
        'mp': [['AA', 'AKs', 'AKo', 'KK', 'QQ', 'AQs', 'JJ'],
               ['AA', 'AKs', 'AKo', 'KK', 'QQ', 'AQs', 'JJ', 'AJs', 'KQs', 'AQo', 'AJo']],
        'co': [['AA', 'AKs', 'AKo', 'KK', 'QQ', 'AQs', 'JJ', 'AJs', 'AQo'],
               ['AA', 'AKs', 'AKo', 'KK', 'QQ', 'AQs', 'JJ', 'AJs', 'KQs', 'AQo', 'AJo', 'KQo', 'KJs', 'QJs']],
        'btn': [['AA', 'AKs', 'AKo', 'KK', 'QQ', 'AQs', 'JJ', 'AJs', 'AQo'],
                ['AA', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s', 'AKo',
                 'KK', 'KQs', 'KJs', 'KTs', 'AQo', 'KQo', 'QQ', 'QJs', 'AJo', 'KJo', 'QJo', 'JJ', 'ATo', 'KTo',
                 'QTo', 'JTo', 'TT', '98s', '97s', '87s', '86s', '76s', '75s', '65s', '64s', '54s']],
        'sb': [['AA', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s', 'AKo',
                'KK', 'KQs', 'KJs', 'KTs', 'AQo', 'KQo', 'QQ', 'QJs', 'AJo', 'KJo', 'QJo', 'JJ', 'ATo', 'KTo',
                'QTo', 'JTo', 'TT', '98s', '97s', '87s', '86s', '76s', '75s', '65s', '64s', '54s'],
               ['AA', 'AKs', 'AKo', 'KK', 'QQ', 'AQs', 'JJ', 'AJs', 'AQo']]
    }
    cards_4bet = {
        'ep': ['AA', 'AKs', 'KK'],
        'mp': ['AA', 'AKs', 'AKo', 'KK'],
        'co': ['AA', 'AKs', 'AKo', 'KK', 'QQ'],
        'btn': ['AA', 'AKs', 'AKo', 'KK', 'QQ', 'JJ'],
        'sb': ['AA', 'AKs', 'AKo', 'KK', 'QQ', 'JJ'],
        'bb': ['AA', 'AKs', 'AKo', 'KK', 'QQ', 'JJ'],
    }

    def __init__(self, cards, position):
        super().__init__(position)
        self.cards = cards
        self.position = position
        self.seat = 5

    def preflop_card(self):
        hand_rank = [card.rank for card in self.cards]
        hand_suit = [card.suit for card in self.cards]
        if hand_rank[0] == hand_rank[1]:
            return hand_rank[0] + hand_rank[1]
        else:
            if self.card_value[hand_rank[0]] > self.card_value[hand_rank[1]]:
                hand_out = hand_rank[0] + hand_rank[1]
            else:
                hand_out = hand_rank[1] + hand_rank[0]
            if hand_suit[0] == hand_suit[1]:
                return hand_out + 's'
            else:
                return hand_out + 'o'

    def fast_fold(self, window):
        if self.position != 'bb':
            if self.preflop_card() not in self.cards_or[self.position] \
                    and self.preflop_card() not in self.cards_cold_call[self.position] \
                    and self.preflop_card() not in self.cards_izolate[self.position]:
                self.fold(window)
                return True

    def fold(self, window):
        time.sleep(1 + random.random())
        stack = []
        while True:
            rect = win32gui.GetWindowRect(window)
            screen = ImageGrab.grab((rect[0], rect[1], rect[2], rect[3]))
            screen_bw = np.array(screen.convert('L'))
            screen_bw = screen_bw[444:444 + 35, 460:547]
            if len(stack) == 2:
                stack.append(screen_bw)
                stack.pop(-2)
                if np.all(stack[0] == stack[1]):
                    pyautogui.press('f1')
                else:
                    break
            else:
                stack.append(screen_bw)
        print('Вы спасовали')
        self.action[self.street].append('F')
        self.in_play = False

    def bet(self, window, bb):
        time.sleep(random.randrange(0, 2) + random.random())
        pyautogui.typewrite(str(bb))
        time.sleep(random.randrange(0, 2) + random.random())
        stack = []
        while True:
            rect = win32gui.GetWindowRect(window)
            screen = ImageGrab.grab((rect[0], rect[1], rect[2], rect[3]))
            screen_bw = np.array(screen.convert('L'))
            screen_bw = screen_bw[527:527 + 20, 471:471 + 131]
            if len(stack) == 2:
                stack.append(screen_bw)
                stack.pop(-2)
                if np.all(stack[0] == stack[1]):
                    pyautogui.press('f3')
                else:
                    break
            else:
                stack.append(screen_bw)
        self.size_bet = bb
        print('Вы поставили ' + str(bb))
        self.action[self.street].append('R')

    def call(self, window, bb):
        time.sleep(random.randrange(1, 3) + random.random())
        stack = []
        while True:
            rect = win32gui.GetWindowRect(window)
            screen = ImageGrab.grab((rect[0], rect[1], rect[2], rect[3]))
            screen_bw = np.array(screen.convert('L'))
            screen_bw = screen_bw[527:527 + 20, 471:471 + 131]
            if len(stack) == 2:
                stack.append(screen_bw)
                stack.pop(-2)
                if np.all(stack[0] == stack[1]):
                    pyautogui.press('f2')
                else:
                    break
            else:
                stack.append(screen_bw)
        self.size_bet = self.size_bet + bb
        print('Вы заколировали +' + str(bb))
        self.action[self.street].append('С')

    def check(self):
        time.sleep(random.randrange(1, 3) + random.random())
        pyautogui.press('f2')
        self.action[self.street].append('X')

    def check_action(self, window, players):
        blinds = ['sb', 'bb']
        actions = [p.action[self.street][-1] for p in players]
        r = len(self.action[self.street])
        # малый блайнд
        if self.position == 'sb' and r == 0:
            self.size_bet = 0.5
            print(self.position + ' Поставил малый блайнд ' + str(self.size_bet))
            self.action[self.street].append('SB')
            return
        # большой блайнд
        if self.position == 'bb' and r == 0:
            self.size_bet = 1
            print(self.position + ' Поставил большой блайнд ' + str(self.size_bet))
            self.action[self.street].append('BB')
            return
        # Open Raise
        if r == 0:
            if len(actions) == 2:
                if self.preflop_card() in self.cards_or[self.position]:
                    self.bet(window, 3)
                    return
        if r == 1:
            if self.position == 'sb' and len(actions) == 1:
                if self.preflop_card() in self.cards_or[self.position]:
                    self.bet(window, 3)
                    return
        # 3 bet
        if r == 0:
            if actions.count('R') == 1 and 'C' not in actions:
                raiser = players[actions.index('R')]
                if raiser.size_bet < 3:
                    if self.preflop_card() in self.cards_3bet[raiser.position][0]:
                        self.bet(window, int(raiser.size_bet * 4))
                        return
                elif raiser.size_bet <= 4:
                    if self.preflop_card() in self.cards_3bet[raiser.position][0]:
                        self.bet(window, int(raiser.size_bet * 3))
                        return
                else:
                    if self.preflop_card() in self.cards_4bet[raiser.position]:
                        self.bet(window, int(self.stack))
                        return
        if r == 1:
            if actions.count('R') == 1 and 'C' not in actions and self.position in blinds:
                raiser = players[actions.index('R')]
                if raiser.size_bet < 3:
                    if self.preflop_card() in self.cards_3bet[raiser.position][1]:
                        self.bet(window, int(raiser.size_bet * 4))
                        return
                elif raiser.size_bet <= 4:
                    if self.preflop_card() in self.cards_3bet[raiser.position][1]:
                        self.bet(window, int(raiser.size_bet * 3))
                        return
                else:
                    if self.preflop_card() in self.cards_4bet[raiser.position]:
                        self.bet(window, int(self.stack))
                        return
        # Колл в холодную
        if r == 0:
            if actions.count('R') == 1:
                if self.preflop_card() in self.cards_cold_call[self.position]:
                    for_call = max([p.size_bet for p in players]) - self.size_bet
                    if for_call < 5:
                        self.call(window, for_call)
                        return
        if r == 1:
            if actions.count('R') == 1 and self.position in blinds:
                if self.preflop_card() in self.cards_cold_call[self.position]:
                    for_call = max([p.size_bet for p in players]) - self.size_bet
                    if for_call < 5:
                        self.call(window, for_call)
                        return

        # Изолейт
        if r == 0:
            if actions.count('R') == 0 and 'C' in actions:
                if self.preflop_card() in self.cards_izolate[self.position]:
                    self.bet(window, 3 + actions.count('C'))
                    return
        if r == 1 and self.position in blinds:
            if actions.count('R') == 0 and 'C' in actions:
                if self.preflop_card() in self.cards_izolate[self.position]:
                    self.bet(window, 3 + actions.count('C'))
                    return
        # сквиз
        if r == 0:
            if actions.count('R') == 1 and 'C' in actions:
                raiser = players[actions.index('R')]
                if self.preflop_card() in self.cards_4bet[self.position]:
                    self.bet(window, int(raiser.size_bet*3 + actions.count('C')))
                    return
        if r == 1:
            if actions.count('R') == 1 and 'C' in actions and self.position in blinds:
                raiser = players[actions.index('R')]
                if self.preflop_card() in self.cards_4bet[self.position]:
                    self.bet(window, int(raiser.size_bet*3 + actions.count('C')))
                    return
        # 4bet
        if r == 1 and self.position not in blinds:
            if self.action[self.street][-1] == 'R' and actions.count('R') == 1:
                size_raise = [p for p in players if p.action[self.street][-1] == 'R'][-1].size_bet
                if size_raise < 10:
                    if self.preflop_card() in self.cards_4bet[self.position]:
                        self.bet(window, int(size_raise * 2.5))
                        return
                else:
                    if self.preflop_card() in self.cards_4bet[self.position]:
                        self.bet(window, int(self.stack))
                        return
        if r == 1 and self.position in blinds:
            if actions.count('R') > 1:
                if self.preflop_card() in self.cards_4bet[self.position]:
                    self.bet(window, int(self.stack))
                    return
        if r == 2 and self.position == 'sb':
            if self.action[self.street][-1] == 'R' and actions.count('R') == 2:
                size_raise = [p for p in players if p.action[self.street][-1] == 'R'][-1].size_bet
                if size_raise < 10:
                    if self.preflop_card() in self.cards_4bet[self.position]:
                        self.bet(window, int(size_raise * 2.5))
                        return
                else:
                    if self.preflop_card() in self.cards_4bet[self.position]:
                        self.bet(window, int(self.stack))
                        return
        # 5bet
        if r == 2 and self.position not in blinds:
            if self.preflop_card() in self.cards_4bet[self.position]:
                self.bet(window, int(self.stack))
                return

        # call preflop push
        if 'R' in actions:
            size_raise = [p for p in players if p.action[self.street][-1] == 'R'][-1].size_bet
            if size_raise > 20:
                if self.preflop_card() in self.cards_4bet[self.position]:
                    self.bet(window, int(self.stack))
                    return
        # check in bb
        if r == 1 and self.position == 'bb':
            if 'R' not in  actions:
                self.check()
                return

        self.fold(window)


    def __str__(self):
        return 'Позиция hero ' + self.position + '\n' \
                                                 'Карты ' + self.preflop_card() + '\n' \
                                                                                  'Стэк ' + str(self.stack)


class Card:
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    suits = ['h', 'd', 'c', 's']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


class FastPoker:
    streets = ['preflop', 'flop', 'turn', 'river']
    positions = ['sb', 'bb', 'ep', 'mp', 'co', 'btn']

    def __init__(self, wind):
        self.hands = []
        self.window = wind
        self.pot = 0
        self.players = []

    def run_hand(self):
        # print(self.hands[-1])
        self.players = []
        self.pot = 0
        btn_chip = self.hands[-1]['btn chip']
        position = self.positions[btn_chip]
        for pos in range(0, 6):
            if pos == self.hands[-1]['btn chip']:
                self.players.append(Hero(cards=self.hands[-1]['hero cards'], position=position))
            else:
                self.players.append(Opp(position=self.positions[pos]))
        seating_list = self.players[btn_chip + 1:] + self.players[:btn_chip]
        for i in range(0, len(seating_list)):
            seating_list[i].seat = i
        for player in self.players:
            player.update_stack(self.window)
        hero = self.players[btn_chip]
        print(hero)
        if not hero.fast_fold(self.window):
            while True:
                for player in self.players:
                    if player.in_play:
                        if not hero.in_play:
                            return

                        max_size_bet = max([player.size_bet for player in self.players])
                        players_playing = [p for p in self.players
                                        if p.in_play if p != player if p.action['preflop']]
                        if player.action['preflop']:
                            if len(players_playing) == 0:
                                print(player.position + ' win')
                                return
                        if player.position == 'sb' or player.position == 'bb':
                            if not player.action['preflop']:
                                player.check_action(self.window, players_playing)
                            else:
                                if player.size_bet == max_size_bet:
                                    self.flop()
                                    return
                                else:
                                    player.check_action(self.window, players_playing)
                        else:
                            if player.size_bet == max_size_bet:
                                self.flop()
                                return
                            else:
                                player.check_action(self.window, players_playing)

                # else:
                #     for player in self.players:
                #         if player.in_play:
                #             if self.playing_count() == 1:
                #                 print('win')
                #                 return
                #             print(player.action)
                #             if player.action['preflop'][-1] == 'R':
                #                 actions = [p.action['preflop'][-1] for p in self.players if p.in_play if p != player]
                #                 if 'R' in actions:
                #                     player.check_action(self.sizing_call(player), r, self.window,actions)
                #                 else:
                #                     print('flop')
                #                     return
                #             else:
                #                 actions = [p.action['preflop'][-1] for p in self.players if p.in_play if p != player]
                #                 player.check_action(self.sizing_call(player), r, self.window, actions)
                #
                #     r += 1

    def flop(self):
        print('********FlOP********')

    def playing_count(self):
        return len([player for player in self.players if player.in_play])


PokerBot().run()
