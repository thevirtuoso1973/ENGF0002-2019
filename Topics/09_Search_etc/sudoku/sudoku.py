from copy import deepcopy
from sys import exit

class Board:
    def __init__(self, board):
        # squares is a list of all 81 squares on the board in row order
        self.squares = []
        for i in range(0,81):
            row = i//9
            col = i%9
            if board[row][col] != "." and board[row][col] != "0":
                self.squares.append([int(board[row][col])])
            else:
                self.squares.append([1,2,3,4,5,6,7,8,9])

        #groups holds all the rows, columns and 3x3 squares
        self.groups = []
        coldata = []
        bigsquaredata = []
        for i in range(0,9):
            coldata.append([])
            bigsquaredata.append([])
        for row in range(0,9):
            rowdata = []
            for col in range(0,9):
                # append a *reference* to the relevant square to the row
                square = self.squares[row*9 + col]
                rowdata.append(square)
                coldata[col].append(square)
                bigrow = row//3
                bigcol = col//3
                bigsquaredata[bigrow*3 + bigcol].append(square)
            self.groups.append(rowdata)
        for i in range(0,9):
            self.groups.append(coldata[i])
        for i in range(0,9):
            self.groups.append(bigsquaredata[i])

    # eliminate values that have already been solved
    def eliminate(self):
        removed = False
        for g in self.groups:
            # go through the group, building a list of already solved values
            already_solved = []
            for square in g:
                if len(square) == 1:
                    already_solved.append(square[0])

            # if an already solved value is in another square in this
            # group, remove it
            for square in g:
                if len(square) > 1:
                    for d in already_solved:
                        if d in square:
                            square.remove(d)
                            removed = True
        return removed

    # if there's only one copy of a value in a group, finalize it.
    def only_one(self):
        removed = False
        for g in self.groups:
            counts = [100]
            for i in range(0,9):
                counts.append(0)
            for square in g:
                if len(square) == 1:
                    counts[square[0]] += 10 # don't bother with this one, it's done
                else:
                    for num in square:
                        counts[num] += 1
            
            for i in range(1,10):
                if counts[i] == 1:
                    for square in g:
                        if i in square:
                            # this is the square that has the only value i,
                            # so remove everything else from this square
                            for num in square.copy():
                                if num != i:
                                    # can't reassign square - need to
                                    # modify the original list
                                    square.remove(num)
                                    removed = True
        return removed

    def check_doubles(self):
        for g in self.groups:
            counts = []
            for i in range(0,9):
                counts.append(0)
            for square in g:
                if len(square) == 1:
                    counts[square[0] - 1] += 1
            for i in range(0,9):
                if counts[i] > 1:
                    #print("count of ", counts[i], "in group", g)
                    return False
        return True

    def eval_move(self):
        progress = True
        while progress:
            progress = self.eliminate()
            progress = progress or self.only_one()
        return self.check_doubles()

    def finished(self):
        for square in self.squares:
            if len(square) != 1:
                return False
        return True
        
    def search(self):
        i = 0
        for square in self.squares:
            if len(square) > 1:
                for value in square:
                    # clone the game so we can test a hypothesis and
                    # roll back if we're wrong
                    clone = deepcopy(self)

                    # test the hypothesis that the i'th square should be 'value'
                    clone.squares[i][:] = [value]

                    # test the consequences of the move
                    result = clone.eval_move()
                    if result == False:
                        #test revealed a wrong move, so try the next option
                        continue

                    # have we finished the board?
                    if clone.finished():
                        print("Finished!")
                        print(clone)
                        return True

                    # OK, not finished, but no immediate
                    # contradiction.  Continue searching from this
                    # position
                    if clone.search():
                        # we finished!
                        return True

                # If we get here, none of these moves worked, so the
                # problem was with an earlier move.  We'll try again
                # from a earlier move.
                return False
            i += 1
        return False
                       
    def __str__(self):
        s = ""
        for row in range(0,9):
            if row == 3 or row == 6:
                s += "---+---+---\n"
            for col in range(0,9):
                if col == 3 or col == 6:
                    s += "|"
                if len(self.groups[row][col]) == 1:
                    s += str(self.groups[row][col][0])
                else:
                    s += "."
            s += "\n"
        return s


initboard = [
    "...251..3",
    ".51......",
    ".2..3....",
    "6..7....8",
    "5.....7.2",
    "1....4..9",
    "....8..9.",
    "......82.",
    "4..312..."]

initboard2 = [
    "8...4127.",
    "......9..",
    "4..7.6...",
    "1.24.....",
    ".6.....8.",
    ".....75.1",
    "...6.9..3",
    "..1......",
    ".4628...5"]

initboard3 = [
    ".9....1..",
    "873.4..9.",
    "..68.....",
    "54.7..8..",
    ".........",
    "..7..4.31",
    ".....89..",
    ".6..7.512",
    "..1....7."]


def loadtests(filename):
    with open(filename, "rt") as f:
        for line in f:
            print(line)
            if len(line) >= 81:
                board = []
                for i in range(0,9):
                    board.append(line[i*9:(i+1)*9])
                game = Board(board)
                print(game)
                game.search()

run_tests = True
if run_tests:
    #loadtests(r"top95")
    loadtests(r"msk_009")
else:
    game = Board(initboard)
    print(game)
    game.search()

