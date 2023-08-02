import numpy as np


class Nonogram:
    def __init__(self, rows, columns):
        self.width = len(columns)
        self.heigth = len(rows)
        self.unknows = self.width * self.heigth

        self.rows = []
        self.columns = []

        self.outputBlack = np.full((self.heigth, self.width), False, dtype=bool)
        self.outputWhite = np.full((self.heigth, self.width), False, dtype=bool)
        self.outputChangeToWhite = []
        self.outputChangeToBlack = []

        for i in range(self.heigth):
            self.rows.append(Line(self.width, rows[i]))

        for i in range(self.width):
            self.columns.append(Line(self.heigth, columns[i]))

    def solveStep(self):
        # Erase falses
        for element in self.outputChangeToWhite:
            x = element[0]
            y = element[1]
            self.rows[x].eraseCombinationWhenTrue(y)
            self.columns[y].eraseCombinationWhenTrue(x)

        # Erase trues
        for element in self.outputChangeToBlack:
            x = element[0]
            y = element[1]
            self.rows[x].eraseCombinationWhenFalse(y)
            self.columns[y].eraseCombinationWhenFalse(x)

        self.outputChangeToWhite.clear()
        self.outputChangeToBlack.clear()

        # Check for "solid" trues in rows
        for i in range(self.heigth):
            a = self.rows[i].combMatrix.all(0)

            for j in range(self.width):
                if self.outputBlack[i, j] == False and a[j] == True:
                    self.outputBlack[i, j] = True
                    self.unknows = self.unknows - 1
                    self.outputChangeToBlack.append([i, j])

        # Check for "solid" trues in columns
        for i in range(self.width):
            a = self.columns[i].combMatrix.all(0)

            for j in range(self.heigth):
                if self.outputBlack[j, i] == False and a[j] == True:
                    self.outputBlack[j, i] = True
                    self.unknows = self.unknows - 1
                    self.outputChangeToBlack.append([j, i])

        # Check for "solid" falses in rows
        for i in range(self.heigth):
            neg = self.rows[i].combMatrix == False
            a = neg.all(0)

            for j in range(self.width):
                if self.outputWhite[i, j] == False and a[j] == True:
                    self.outputWhite[i, j] = True
                    self.unknows = self.unknows - 1
                    self.outputChangeToWhite.append([i, j])

        # Check for "solid" falses in columns
        for i in range(self.width):
            neg = self.columns[i].combMatrix == False
            a = neg.all(0)

            for j in range(self.heigth):
                if self.outputWhite[j, i] == False and a[j] == True:
                    self.outputWhite[j, i] = True
                    self.unknows = self.unknows - 1
                    self.outputChangeToWhite.append([j, i])


class Line:
    def __init__(self, length, elements):
        self.elements = elements
        self.length = length
        self.distances = []
        self.numOfCombinations = 0

        self.fillDistances(self.length - sum(self.elements), len(self.elements))
        self.fillCombinations()

    def fillDistances(self, distanceSum, numOfElements, currentLine=[]):
        if len(currentLine) == 0:
            currentLine = [0]
            for i in range(0, (distanceSum - numOfElements + 2)):
                currentLine[0] = i
                self.fillDistances(distanceSum, numOfElements, currentLine.copy())

        elif len(currentLine) > 0 and len(currentLine) < numOfElements:
            currentLine.append(0)
            for i in range(1, (distanceSum - sum(currentLine) + 1)):
                currentLine[-1] = i
                self.fillDistances(distanceSum, numOfElements, currentLine.copy())

        else:
            self.distances.append(currentLine.copy())

    def fillLine(self, distances):
        line = []

        for i in range(len(self.elements)):
            line.extend([False] * distances[i])
            line.extend([True] * self.elements[i])

        line.extend([False] * (self.length - len(line)))
        line = np.array(line)

        return line

    def fillCombinations(self):
        self.numOfCombinations = len(self.distances)
        self.combMatrix = np.full((self.numOfCombinations, self.length), False, dtype=bool)

        for i in range(self.numOfCombinations):
            self.combMatrix[i, :] = self.fillLine(self.distances[i])

    def eraseCombinationWhenTrue(self, element):
        linesToErase = []
        for i in range(self.numOfCombinations):
            if self.combMatrix[i, element] == True:
                linesToErase.append(i)

        self.combMatrix = np.delete(self.combMatrix, linesToErase, 0)
        self.numOfCombinations = self.combMatrix.shape[0]

    def eraseCombinationWhenFalse(self, element):
        linesToErase = []
        for i in range(self.numOfCombinations):
            if self.combMatrix[i, element] == False:
                linesToErase.append(i)

        self.combMatrix = np.delete(self.combMatrix, linesToErase, 0)
        self.numOfCombinations = self.combMatrix.shape[0]
