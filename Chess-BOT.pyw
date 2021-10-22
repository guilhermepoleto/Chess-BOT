import pyautogui as pg
import time
import sys
from stockfish import Stockfish
from win10toast import ToastNotifier
import PySimpleGUI as ps
import keyboard

try:
    ps.theme('Reddit')
    layout = [
        [ps.Text('Playing')],
        [ps.Button('White')],
        [ps.Button('Black')],
        [ps.Text('Skill level: '), ps.Input(key='skill')],
        [ps.Text('Tempo (s): '), ps.Input(key='tempo')],
    ]
    janela = ps.Window('CHESS BOT', layout)

    while True:
        eventos, valores = janela.read()
        if eventos == ps.WINDOW_CLOSED:
            break
        if eventos == 'White':
            playing = "w"
            skill = valores['skill']
            time = valores['tempo']
            janela.close()
        if eventos == 'Black':
            playing = "b"
            skill = valores['skill']
            time = valores['tempo']
            janela.close()

    print(float(time) * 1000)
    path = YOUR_PATH_TO_STOCKFISH
    stockfish = Stockfish(path)
    stockfish.set_skill_level(skill)
    toast = ToastNotifier()
    move = ""

    def getMove():

        c = 0
        n = 1

        startFen = "00000000/00000000/00000000/00000000/00000000/00000000/00000000/00000000X"
        listFen = []
        listFen[:0] = startFen

        for pos in pg.locateAllOnScreen('torreW.png', confidence=0.93, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "R"

        for pos in pg.locateAllOnScreen('damaW.png', confidence=0.93, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "Q"

        for pos in pg.locateAllOnScreen('reiW.png', confidence=0.9, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "K"
        for pos in pg.locateAllOnScreen('cavaloW.png', confidence=0.93, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "N"
            
        for pos in pg.locateAllOnScreen('bispoW.png', confidence=0.925, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "B"

        for pos in pg.locateAllOnScreen('peaoW.png', confidence=0.93, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "P"

        #-------------------------------------------- BLACK PIECES ----------------------------

        for pos in pg.locateAllOnScreen('peaoB.png', confidence=0.98, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "p"

        for pos in pg.locateAllOnScreen('torreB.png', confidence=0.98, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "r"

        for pos in pg.locateAllOnScreen('cavaloB.png', confidence=0.96, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "n"

        for pos in pg.locateAllOnScreen('bispoB.png', confidence=0.98, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "b"

        for pos in pg.locateAllOnScreen('damaB.png', confidence=0.8, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "q"

        for pos in pg.locateAllOnScreen('reiB.png', confidence=0.96, region=(315,169,800,800)):
            x,y = pg.center(pos)
            linha = int(y/100)-2
            coluna = int(x/100)-3
            listFen[9*linha + coluna] = "k"

        for elementos in listFen:
            if elementos == "0":
                index = getIndex(listFen) 
                while listFen[index+1] == "0":
                    n += 1
                    index += 1
                for x in range(0,n):
                    listFen.pop(c)
                listFen.insert(c,str(n))
                n = 1
            c += 1

        listFen.pop()
        if playing == "b":
            listFen.reverse()
        strFen = listToString(listFen)
        fen = strFen + " " + playing + " - - 0 1"
        stockfish.set_fen_position(fen)
        m = stockfish.get_best_move_time(float(time) * 1000)
        e = stockfish.get_evaluation()
        return m,e

    def listToString(s): 
        
        str1 = ""  
        for ele in s: 
            str1 += ele  
        return str1

    def getIndex(lst):
        c = 0
        for e in lst:
            if e == "0":
                return c
            c += 1

    cordenadasColunasW = {"a": 365, "b": 465, "c": 565, "d": 665, "e": 765, "f": 865, "g": 965, "h": 1065}
    cordenadasLinhasW = {"1": 920, "2": 820, "3": 720, "4": 620, "5": 520, "6": 420, "7": 320, "8": 220}
    cordenadasColunasB = {"a": 1065, "b": 965, "c": 865, "d": 765, "e": 665, "f": 565, "g": 465, "h": 365}
    cordenadasLinhasB = {"1": 220, "2": 320, "3": 420, "4": 520, "5": 620, "6": 720, "7": 820, "8": 920}

    while True:

        if keyboard.is_pressed('e') == True:
            move,e = getMove()
            if playing == "w":
                pg.moveTo(cordenadasColunasW[move[0]],cordenadasLinhasW[move[1]])
                pg.mouseDown();
                pg.moveTo(cordenadasColunasW[move[2]],cordenadasLinhasW[move[3]])
                pg.mouseUp();
            if playing == "b":
                pg.moveTo(cordenadasColunasB[move[0]],cordenadasLinhasB[move[1]])
                pg.mouseDown();
                pg.moveTo(cordenadasColunasB[move[2]],cordenadasLinhasB[move[3]])
                pg.mouseUp();

        if keyboard.is_pressed('q') == True:
            
            move,evaluation = getMove()
            toast.show_toast("Move:",f"Lance: {move} - Barrinha: {evaluation['value']}",duration=3)


        if keyboard.is_pressed('z') == True:
            stockfish.__del__()
            sys.exit()
except:
    stockfish.__del__()
    sys.exit()
