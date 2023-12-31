import nonogram
import matplotlib.pyplot as plt

rows = [[4],
        [2, 1, 1],
        [3, 3],
        [10],
        [2, 4, 2],
        [4, 2, 1],
        [6, 2],
        [7, 2],
        [7, 1],
        [7, 2],
        [6, 2],
        [6, 2],
        [5, 2, 6],
        [9, 7],
        [8, 4],
        [3, 3, 5],
        [2, 3, 2, 1],
        [2, 3],
        [1, 2],
        [2]]

colums = [[1],
          [2],
          [2],
          [3],
          [4, 3],
          [9],
          [10],
          [10, 1],
          [10, 2],
          [8, 3, 2],
          [8, 2, 3],
          [1, 5, 7],
          [2, 3, 2, 2],
          [4, 2, 4],
          [10, 3],
          [1, 5, 2],
          [2, 2, 2],
          [1, 2, 2],
          [5, 2],
          [3, 2]]

nono = nonogram.Nonogram(rows, colums)

plt.spy(nono.outputBlack)
plt.title(nono.unknows)
plt.pause(5)

while (nono.unknows):
    nono.solveStep()
    plt.cla()  # delete previous plot
    plt.spy(nono.outputBlack)
    plt.title(nono.unknows)
    plt.pause(0.5)
