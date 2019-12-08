import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
import mainwindow
import cards_dialog


class MainApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.open_raise_cards = {'EP': [], 'MP': [], 'CO': [], 'BTN': [], 'SB': []}
        self.pushButton.clicked.connect(lambda: self.open_cards_dialog(self.pushButton))
        self.pushButton_2.clicked.connect(lambda: self.open_cards_dialog(self.pushButton_2))
        self.pushButton_3.clicked.connect(lambda: self.open_cards_dialog(self.pushButton_3))
        self.pushButton_4.clicked.connect(lambda: self.open_cards_dialog(self.pushButton_4))
        self.pushButton_5.clicked.connect(lambda: self.open_cards_dialog(self.pushButton_5))
        self.update_opening_range()

    def open_cards_dialog(self, button):
        dialog = CardApp('OR', button.text(), self.open_raise_cards[button.text()])
        dialog.exec_()
        self.open_raise_cards[button.text()] = dialog.cards
        self.update_opening_range()

    # комбинаторика  С(n,m) = n!/m!(n-m)!
    def update_opening_range(self):
        buttons = [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.pushButton_5]
        # количество пар С(4,2) = 6, 6*13(кол-во номиналов) = 78
        # непары С(52,2) = 1326, 1326 - 78 = 1248
        # одномастные  С(13,2)*4 = 312
        # разномастные 1248 - 312 = 936
        for button in buttons:
            if self.open_raise_cards[button.text()]:
                count = 0
                for card in self.open_raise_cards[button.text()]:
                    if card[0] == card[1]:
                        count += 6
                    elif card[-1] == 's':
                        count += 4
                    elif card[-1] == 'o':
                        count += 12
                opening_range = 100*count/1326
                print(opening_range)



class CardApp(QtWidgets.QDialog, cards_dialog.Ui_Dialog):
    def __init__(self, action, position,cards):
        super().__init__()
        self.action = action
        self.position = position
        self.setupUi(self)
        self.cards = cards
        self.buttonBox.accepted.connect(self.test)
        self.textEdit.setText(str(self.cards))
        # почему не работает циклом?
        self.buttons[0][0].clicked.connect(lambda: self.add_card(self.buttons[0][0]))
        self.buttons[0][1].clicked.connect(lambda: self.add_card(self.buttons[0][1]))
        self.buttons[0][2].clicked.connect(lambda: self.add_card(self.buttons[0][2]))
        self.buttons[0][3].clicked.connect(lambda: self.add_card(self.buttons[0][3]))
        self.buttons[0][4].clicked.connect(lambda: self.add_card(self.buttons[0][4]))
        self.buttons[0][5].clicked.connect(lambda: self.add_card(self.buttons[0][5]))
        self.buttons[0][6].clicked.connect(lambda: self.add_card(self.buttons[0][6]))
        self.buttons[0][7].clicked.connect(lambda: self.add_card(self.buttons[0][7]))
        self.buttons[0][8].clicked.connect(lambda: self.add_card(self.buttons[0][8]))
        self.buttons[0][9].clicked.connect(lambda: self.add_card(self.buttons[0][9]))
        self.buttons[0][10].clicked.connect(lambda: self.add_card(self.buttons[0][10]))
        self.buttons[0][11].clicked.connect(lambda: self.add_card(self.buttons[0][11]))
        self.buttons[0][12].clicked.connect(lambda: self.add_card(self.buttons[0][12]))
        self.buttons[1][0].clicked.connect(lambda: self.add_card(self.buttons[1][0]))
        self.buttons[1][1].clicked.connect(lambda: self.add_card(self.buttons[1][1]))
        self.buttons[1][2].clicked.connect(lambda: self.add_card(self.buttons[1][2]))
        self.buttons[1][3].clicked.connect(lambda: self.add_card(self.buttons[1][3]))
        self.buttons[1][4].clicked.connect(lambda: self.add_card(self.buttons[1][4]))
        self.buttons[1][5].clicked.connect(lambda: self.add_card(self.buttons[1][5]))
        self.buttons[1][6].clicked.connect(lambda: self.add_card(self.buttons[1][6]))
        self.buttons[1][7].clicked.connect(lambda: self.add_card(self.buttons[1][7]))
        self.buttons[1][8].clicked.connect(lambda: self.add_card(self.buttons[1][8]))
        self.buttons[1][9].clicked.connect(lambda: self.add_card(self.buttons[1][9]))
        self.buttons[1][10].clicked.connect(lambda: self.add_card(self.buttons[1][10]))
        self.buttons[1][11].clicked.connect(lambda: self.add_card(self.buttons[1][11]))
        self.buttons[1][12].clicked.connect(lambda: self.add_card(self.buttons[1][12]))
        self.buttons[2][0].clicked.connect(lambda: self.add_card(self.buttons[2][0]))
        self.buttons[2][1].clicked.connect(lambda: self.add_card(self.buttons[2][1]))
        self.buttons[2][2].clicked.connect(lambda: self.add_card(self.buttons[2][2]))
        self.buttons[2][3].clicked.connect(lambda: self.add_card(self.buttons[2][3]))
        self.buttons[2][4].clicked.connect(lambda: self.add_card(self.buttons[2][4]))
        self.buttons[2][5].clicked.connect(lambda: self.add_card(self.buttons[2][5]))
        self.buttons[2][6].clicked.connect(lambda: self.add_card(self.buttons[2][6]))
        self.buttons[2][7].clicked.connect(lambda: self.add_card(self.buttons[2][7]))
        self.buttons[2][8].clicked.connect(lambda: self.add_card(self.buttons[2][8]))
        self.buttons[2][9].clicked.connect(lambda: self.add_card(self.buttons[2][9]))
        self.buttons[2][10].clicked.connect(lambda: self.add_card(self.buttons[2][10]))
        self.buttons[2][11].clicked.connect(lambda: self.add_card(self.buttons[2][11]))
        self.buttons[2][12].clicked.connect(lambda: self.add_card(self.buttons[2][12]))
        self.buttons[3][0].clicked.connect(lambda: self.add_card(self.buttons[3][0]))
        self.buttons[3][1].clicked.connect(lambda: self.add_card(self.buttons[3][1]))
        self.buttons[3][2].clicked.connect(lambda: self.add_card(self.buttons[3][2]))
        self.buttons[3][3].clicked.connect(lambda: self.add_card(self.buttons[3][3]))
        self.buttons[3][4].clicked.connect(lambda: self.add_card(self.buttons[3][4]))
        self.buttons[3][5].clicked.connect(lambda: self.add_card(self.buttons[3][5]))
        self.buttons[3][6].clicked.connect(lambda: self.add_card(self.buttons[3][6]))
        self.buttons[3][7].clicked.connect(lambda: self.add_card(self.buttons[3][7]))
        self.buttons[3][8].clicked.connect(lambda: self.add_card(self.buttons[3][8]))
        self.buttons[3][9].clicked.connect(lambda: self.add_card(self.buttons[3][9]))
        self.buttons[3][10].clicked.connect(lambda: self.add_card(self.buttons[3][10]))
        self.buttons[3][11].clicked.connect(lambda: self.add_card(self.buttons[3][11]))
        self.buttons[3][12].clicked.connect(lambda: self.add_card(self.buttons[3][12]))
        self.buttons[4][0].clicked.connect(lambda: self.add_card(self.buttons[4][0]))
        self.buttons[4][1].clicked.connect(lambda: self.add_card(self.buttons[4][1]))
        self.buttons[4][2].clicked.connect(lambda: self.add_card(self.buttons[4][2]))
        self.buttons[4][3].clicked.connect(lambda: self.add_card(self.buttons[4][3]))
        self.buttons[4][4].clicked.connect(lambda: self.add_card(self.buttons[4][4]))
        self.buttons[4][5].clicked.connect(lambda: self.add_card(self.buttons[4][5]))
        self.buttons[4][6].clicked.connect(lambda: self.add_card(self.buttons[4][6]))
        self.buttons[4][7].clicked.connect(lambda: self.add_card(self.buttons[4][7]))
        self.buttons[4][8].clicked.connect(lambda: self.add_card(self.buttons[4][8]))
        self.buttons[4][9].clicked.connect(lambda: self.add_card(self.buttons[4][9]))
        self.buttons[4][10].clicked.connect(lambda: self.add_card(self.buttons[4][10]))
        self.buttons[4][11].clicked.connect(lambda: self.add_card(self.buttons[4][11]))
        self.buttons[4][12].clicked.connect(lambda: self.add_card(self.buttons[4][12]))
        self.buttons[5][0].clicked.connect(lambda: self.add_card(self.buttons[5][0]))
        self.buttons[5][1].clicked.connect(lambda: self.add_card(self.buttons[5][1]))
        self.buttons[5][2].clicked.connect(lambda: self.add_card(self.buttons[5][2]))
        self.buttons[5][3].clicked.connect(lambda: self.add_card(self.buttons[5][3]))
        self.buttons[5][4].clicked.connect(lambda: self.add_card(self.buttons[5][4]))
        self.buttons[5][5].clicked.connect(lambda: self.add_card(self.buttons[5][5]))
        self.buttons[5][6].clicked.connect(lambda: self.add_card(self.buttons[5][6]))
        self.buttons[5][7].clicked.connect(lambda: self.add_card(self.buttons[5][7]))
        self.buttons[5][8].clicked.connect(lambda: self.add_card(self.buttons[5][8]))
        self.buttons[5][9].clicked.connect(lambda: self.add_card(self.buttons[5][9]))
        self.buttons[5][10].clicked.connect(lambda: self.add_card(self.buttons[5][10]))
        self.buttons[5][11].clicked.connect(lambda: self.add_card(self.buttons[5][11]))
        self.buttons[5][12].clicked.connect(lambda: self.add_card(self.buttons[5][12]))
        self.buttons[6][0].clicked.connect(lambda: self.add_card(self.buttons[6][0]))
        self.buttons[6][1].clicked.connect(lambda: self.add_card(self.buttons[6][1]))
        self.buttons[6][2].clicked.connect(lambda: self.add_card(self.buttons[6][2]))
        self.buttons[6][3].clicked.connect(lambda: self.add_card(self.buttons[6][3]))
        self.buttons[6][4].clicked.connect(lambda: self.add_card(self.buttons[6][4]))
        self.buttons[6][5].clicked.connect(lambda: self.add_card(self.buttons[6][5]))
        self.buttons[6][6].clicked.connect(lambda: self.add_card(self.buttons[6][6]))
        self.buttons[6][7].clicked.connect(lambda: self.add_card(self.buttons[6][7]))
        self.buttons[6][8].clicked.connect(lambda: self.add_card(self.buttons[6][8]))
        self.buttons[6][9].clicked.connect(lambda: self.add_card(self.buttons[6][9]))
        self.buttons[6][10].clicked.connect(lambda: self.add_card(self.buttons[6][10]))
        self.buttons[6][11].clicked.connect(lambda: self.add_card(self.buttons[6][11]))
        self.buttons[6][12].clicked.connect(lambda: self.add_card(self.buttons[6][12]))
        self.buttons[7][0].clicked.connect(lambda: self.add_card(self.buttons[7][0]))
        self.buttons[7][1].clicked.connect(lambda: self.add_card(self.buttons[7][1]))
        self.buttons[7][2].clicked.connect(lambda: self.add_card(self.buttons[7][2]))
        self.buttons[7][3].clicked.connect(lambda: self.add_card(self.buttons[7][3]))
        self.buttons[7][4].clicked.connect(lambda: self.add_card(self.buttons[7][4]))
        self.buttons[7][5].clicked.connect(lambda: self.add_card(self.buttons[7][5]))
        self.buttons[7][6].clicked.connect(lambda: self.add_card(self.buttons[7][6]))
        self.buttons[7][7].clicked.connect(lambda: self.add_card(self.buttons[7][7]))
        self.buttons[7][8].clicked.connect(lambda: self.add_card(self.buttons[7][8]))
        self.buttons[7][9].clicked.connect(lambda: self.add_card(self.buttons[7][9]))
        self.buttons[7][10].clicked.connect(lambda: self.add_card(self.buttons[7][10]))
        self.buttons[7][11].clicked.connect(lambda: self.add_card(self.buttons[7][11]))
        self.buttons[7][12].clicked.connect(lambda: self.add_card(self.buttons[7][12]))
        self.buttons[8][0].clicked.connect(lambda: self.add_card(self.buttons[8][0]))
        self.buttons[8][1].clicked.connect(lambda: self.add_card(self.buttons[8][1]))
        self.buttons[8][2].clicked.connect(lambda: self.add_card(self.buttons[8][2]))
        self.buttons[8][3].clicked.connect(lambda: self.add_card(self.buttons[8][3]))
        self.buttons[8][4].clicked.connect(lambda: self.add_card(self.buttons[8][4]))
        self.buttons[8][5].clicked.connect(lambda: self.add_card(self.buttons[8][5]))
        self.buttons[8][6].clicked.connect(lambda: self.add_card(self.buttons[8][6]))
        self.buttons[8][7].clicked.connect(lambda: self.add_card(self.buttons[8][7]))
        self.buttons[8][8].clicked.connect(lambda: self.add_card(self.buttons[8][8]))
        self.buttons[8][9].clicked.connect(lambda: self.add_card(self.buttons[8][9]))
        self.buttons[8][10].clicked.connect(lambda: self.add_card(self.buttons[8][10]))
        self.buttons[8][11].clicked.connect(lambda: self.add_card(self.buttons[8][11]))
        self.buttons[8][12].clicked.connect(lambda: self.add_card(self.buttons[8][12]))
        self.buttons[9][0].clicked.connect(lambda: self.add_card(self.buttons[9][0]))
        self.buttons[9][1].clicked.connect(lambda: self.add_card(self.buttons[9][1]))
        self.buttons[9][2].clicked.connect(lambda: self.add_card(self.buttons[9][2]))
        self.buttons[9][3].clicked.connect(lambda: self.add_card(self.buttons[9][3]))
        self.buttons[9][4].clicked.connect(lambda: self.add_card(self.buttons[9][4]))
        self.buttons[9][5].clicked.connect(lambda: self.add_card(self.buttons[9][5]))
        self.buttons[9][6].clicked.connect(lambda: self.add_card(self.buttons[9][6]))
        self.buttons[9][7].clicked.connect(lambda: self.add_card(self.buttons[9][7]))
        self.buttons[9][8].clicked.connect(lambda: self.add_card(self.buttons[9][8]))
        self.buttons[9][9].clicked.connect(lambda: self.add_card(self.buttons[9][9]))
        self.buttons[9][10].clicked.connect(lambda: self.add_card(self.buttons[9][10]))
        self.buttons[9][11].clicked.connect(lambda: self.add_card(self.buttons[9][11]))
        self.buttons[9][12].clicked.connect(lambda: self.add_card(self.buttons[9][12]))
        self.buttons[10][0].clicked.connect(lambda: self.add_card(self.buttons[10][0]))
        self.buttons[10][1].clicked.connect(lambda: self.add_card(self.buttons[10][1]))
        self.buttons[10][2].clicked.connect(lambda: self.add_card(self.buttons[10][2]))
        self.buttons[10][3].clicked.connect(lambda: self.add_card(self.buttons[10][3]))
        self.buttons[10][4].clicked.connect(lambda: self.add_card(self.buttons[10][4]))
        self.buttons[10][5].clicked.connect(lambda: self.add_card(self.buttons[10][5]))
        self.buttons[10][6].clicked.connect(lambda: self.add_card(self.buttons[10][6]))
        self.buttons[10][7].clicked.connect(lambda: self.add_card(self.buttons[10][7]))
        self.buttons[10][8].clicked.connect(lambda: self.add_card(self.buttons[10][8]))
        self.buttons[10][9].clicked.connect(lambda: self.add_card(self.buttons[10][9]))
        self.buttons[10][10].clicked.connect(lambda: self.add_card(self.buttons[10][10]))
        self.buttons[10][11].clicked.connect(lambda: self.add_card(self.buttons[10][11]))
        self.buttons[10][12].clicked.connect(lambda: self.add_card(self.buttons[10][12]))
        self.buttons[11][0].clicked.connect(lambda: self.add_card(self.buttons[11][0]))
        self.buttons[11][1].clicked.connect(lambda: self.add_card(self.buttons[11][1]))
        self.buttons[11][2].clicked.connect(lambda: self.add_card(self.buttons[11][2]))
        self.buttons[11][3].clicked.connect(lambda: self.add_card(self.buttons[11][3]))
        self.buttons[11][4].clicked.connect(lambda: self.add_card(self.buttons[11][4]))
        self.buttons[11][5].clicked.connect(lambda: self.add_card(self.buttons[11][5]))
        self.buttons[11][6].clicked.connect(lambda: self.add_card(self.buttons[11][6]))
        self.buttons[11][7].clicked.connect(lambda: self.add_card(self.buttons[11][7]))
        self.buttons[11][8].clicked.connect(lambda: self.add_card(self.buttons[11][8]))
        self.buttons[11][9].clicked.connect(lambda: self.add_card(self.buttons[11][9]))
        self.buttons[11][10].clicked.connect(lambda: self.add_card(self.buttons[11][10]))
        self.buttons[11][11].clicked.connect(lambda: self.add_card(self.buttons[11][11]))
        self.buttons[11][12].clicked.connect(lambda: self.add_card(self.buttons[11][12]))
        self.buttons[12][0].clicked.connect(lambda: self.add_card(self.buttons[12][0]))
        self.buttons[12][1].clicked.connect(lambda: self.add_card(self.buttons[12][1]))
        self.buttons[12][2].clicked.connect(lambda: self.add_card(self.buttons[12][2]))
        self.buttons[12][3].clicked.connect(lambda: self.add_card(self.buttons[12][3]))
        self.buttons[12][4].clicked.connect(lambda: self.add_card(self.buttons[12][4]))
        self.buttons[12][5].clicked.connect(lambda: self.add_card(self.buttons[12][5]))
        self.buttons[12][6].clicked.connect(lambda: self.add_card(self.buttons[12][6]))
        self.buttons[12][7].clicked.connect(lambda: self.add_card(self.buttons[12][7]))
        self.buttons[12][8].clicked.connect(lambda: self.add_card(self.buttons[12][8]))
        self.buttons[12][9].clicked.connect(lambda: self.add_card(self.buttons[12][9]))
        self.buttons[12][10].clicked.connect(lambda: self.add_card(self.buttons[12][10]))
        self.buttons[12][11].clicked.connect(lambda: self.add_card(self.buttons[12][11]))
        self.buttons[12][12].clicked.connect(lambda: self.add_card(self.buttons[12][12]))
        for r in range(0, 13):
            for c in range(0, 13):
                if self.cards_str[r][c] in self.cards:
                    self.buttons[r][c].setChecked(True)

    def add_card(self, button):
        if button.text() in self.cards:
            self.cards.remove(button.text())
        else:
            self.cards.append(button.text())
        self.textEdit.setText(str(self.cards))

    def test(self):
        print('ok')

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()