import struct # Импортировали модуль для работы с двоичными записями.
import os
import pandas as pd
from terminaltables import AsciiTable
import uuid
import copy

def generatePrintTable(PField):
    resultTable = AsciiTable(PField)
    resultTable.inner_heading_row_border = True
    resultTable.outer_border = True
    resultTable.inner_row_border = True
    print(resultTable.table)


class PlayField():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.playFieldArea = []
        for i in range(y):
            self.playFieldArea.append([x for x in ' ' * x])

    def printField(self):
        return generatePrintTable(self.playFieldArea)

    def fillField(self, x, y, value):
        # print(f'{x},{y}')
        self.playFieldArea[x][y] = value

    def prepareAvailableSteps(self):
        for y in range(self.y):
            for x in range(self.x):
                if not self.playFieldArea[y][x].number == '0':
                    #newCopyplayFieldArea = copy.deepcopy(self.playFieldArea)
                    decideList = []
                    # print(f'x={x}, y={y}')
                    stepList = [{'y': y, 'x': x}]
                    if not self.playFieldArea[y][x].number == '1':
                        self.foundConnection(self.playFieldArea, x, y, decideList, stepList,
                        self.playFieldArea[y][x].number)
                    else:
                        decideList.append(stepList)
                    print(f'x={x}, y={y}, n={self.playFieldArea[y][x].number}, len={len(decideList)}')
                    #newCopyplayFieldArea = None

    def foundConnection(self, playFieldArea, x, y, decideList, stepList, number):
        countSteps = int(number) - len(stepList)

        steps = []
        steps.append({'x': -1, 'y': 0, 'side': 'L'})
        steps.append({'x': 1, 'y': 0, 'side': 'R'})
        steps.append({'x': 0, 'y': -1, 'side': 'U'})
        steps.append({'x': 0, 'y': 1, 'side': 'D'})
        if countSteps > 0:
            for currentStep in steps:
                # print(currentStep)
                side = currentStep.get('side')
                xAdd = currentStep.get('x')
                yAdd = currentStep.get('y')
                if playFieldArea[y][x].canStep(side):
                    have_step = stepList.count({'y': (y + yAdd), 'x': (x + xAdd)})
                    if have_step == 0 and playFieldArea[y + yAdd][x + xAdd].number == '0' and not countSteps == 1:
                        newStepList = copy.copy(stepList)
                        newStepList.append({'y': (y + yAdd), 'x': (x + xAdd)})
                        self.foundConnection(playFieldArea, x + xAdd, y + yAdd, decideList, newStepList, number)
                    elif playFieldArea[y + yAdd][x + xAdd].number == number and countSteps == 1:
                        decideList.append(stepList + [{'y': (y + yAdd), 'x': (x + xAdd)}])


class Cells(object):
    def __init__(self, x, y, number, color, rest, xMax, yMax):
        self.x = x
        self.y = y
        self.color = color
        self.number = number
        self.rest = rest
        if number == '0':
            self.countSteps = 0
        else:
            self.countSteps = int(number) - 1
        self.canLeft = True
        self.canRight = True
        self.canUp = True
        self.canDown = True
        self.decideList = []
        if not number == '0':
            self.uuid = uuid.uuid1()
        else:
            self.uuid = None

        if not rest == '':
            if rest == '8':
                self.canDown = False
            elif rest == '2':
                self.canUp = False
            elif rest == '4':
                self.canRight = False
            elif rest == '1':
                self.canLeft = False
            elif rest == '11':
                self.canUp = False
                self.canLeft = False
                self.canDown = False
            elif rest == '12':
                self.canRight = False
                self.canDown = False
            elif rest == '9':
                self.canLeft = False
                self.canDown = False
            elif rest == '6':
                self.canRight = False
                self.canUp = False
            elif rest == '6':
                self.canRight = False
                self.canLeft = False
            if x == 0:
                self.canLeft = False
            if y == 0:
                self.canUp = False
            if x == xMax - 1:
                self.canRight = False
            if y == yMax - 1:
                self.canDown = False

    def __str__(self):
        if self.number == '0':
            number = ''
        else:
            number = self.number
        strRest = ''
        if not self.canDown:
            strRest += 'D'
        if not self.canUp:
            strRest += 'U'
        if not self.canRight:
            strRest += 'R'
        if not self.canLeft:
            strRest += 'L'
        if self.number == '0':
            color = ''
        else:
            color = self.color
        if not number == '' and strRest == '':
            return f'{number}\n{color}'
        elif not number == '' and not strRest == '':
            return f'{number}\n{color}\n{strRest}'
        elif number == '' and not strRest == '':
            #            strRest = ''
            #            if not self.canDown:
            #                strRest.join('D')
            #            if not self.canUp:
            #                strRest.join('U')
            #            if not self.canRight:
            #                strRest.join('R')
            #            if not self.canLeft:
            #                strRest.join('L')
            return f'\n\n{strRest}'
        else:
            return ''

    def addDecide(self):
        pass

    def canStep(self, side):
        if side == 'L':
            return self.canLeft
        if side == 'R':
            return self.canRight
        if side == 'U':
            return self.canUp
        if side == 'D':
            return self.canDown



def main():
    path = 'F:\\Tests\\APKTool\\PathPix.Pro.v.1.1.3.b.1021.Permissions.Removed\\assets\\puzzles\\'
    listOfFiles = os.listdir(path)
    columnlist = ['filename', 'x', 'y', 'message', 'byte']
    counter = 0
    df = pd.DataFrame(columns=columnlist)
    maxByte = 0
    for currentFile in listOfFiles:
        if currentFile[-5:] != 't.ppx' and currentFile[:3] == '001':
            with open(path + currentFile, 'rb') as fppx:
                # byte = fppx.read(8)
                byte = fppx.read()
                maxByte = max(len(byte), maxByte)
                first = byte[:22]
                print(currentFile)
                # print(str(byte[22:]) + '\n\n')
                for i in range(22, 230):
                    if byte[i + 1: i + 5] == b'\xff\xff\xff\xff':
                        break
                message = byte[22:i]
                i += 4
                # print(str(message))
                print([int(x) for x in byte[i + 2:i + 100]])
                df.loc[counter] = [currentFile, first[16], first[14], str(message), str([int(x) for x in byte[i + 2:]])]
                counter += 1
    #print(maxByte)
    byteset = df['byte'][0][1:-1].split(', ')
    playField = PlayField(int(df['x'][0]), int(df['y'][0]))


    df2 = pd.DataFrame(columns=['x','y','b1','b2','b3','b4','b5','b6'])
    bytesetlen = len(byteset)
    counter = 24
    pCounter = 0
    curX = 0
    curY = 0
    while True:
        if counter > bytesetlen:
            break
        else:
            dataset = byteset[counter:counter + 6]
            counter += 6
            playField.fillField(curY, curX, Cells(curX, curY, dataset[0], dataset[1], dataset[4], playField.x, playField.y))
            if curX >= playField.x - 1:
                curY += 1
                curX = 0
            else:
                curX += 1

    playField.prepareAvailableSteps()

main()