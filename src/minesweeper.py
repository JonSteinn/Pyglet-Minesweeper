from random import uniform

class MinesweeperSquare:
    def __init__(self, adjacency_count=0, flipped=False, marked=False):
        self.ac = adjacency_count
        self.flipped = flipped
        self.marked = marked

    def flip(self):
        self.flipped = not self.flipped

    def increment_adjacency_count(self):
        self.ac += 1

    def make_bomb(self):
        self.ac = -1

    def is_bomb(self):
        return self.ac == -1

    def is_visible(self):
        return self.flipped

    def adjacent_bombs(self):
        return self.ac

    def mark(self):
        self.marked = True

    def unmark(self):
        self.marked = False

    def is_marked(self):
        return self.marked




class Minesweeper:
    ROW_SIZE = 16
    COL_SIZE = 16
    TOTAL_BOMBS = 40

    WON,LOST,ONGOING = range(3)

    def __init__(self, r, c):
        self.mat = [[MinesweeperSquare()]*Minesweeper.COL_SIZE for _ in range(Minesweeper.ROW_SIZE)]
        self.status = Minesweeper.ONGOING
        self.bombs_rem = Minesweeper.TOTAL_BOMBS

    def neighbors(self, r, c):
        for _r, _c in zip((-1,0,1),(-1,0,1)):
            if _r and _c and 0 <= _r < Minesweeper.ROW_SIZE and 0 <= _c < Minesweeper.COL_SIZE:
                yield r+_r,c+_c

    def generate(self, r, c):
        cnt = 0
        while cnt < 40:
            _r = int(uniform(0, Minesweeper.ROW_SIZE))
            _c = int(uniform(0, Minesweeper.COL_SIZE))
            if (_r==r and _c == c) or self.mat[_r][_c].is_bomb():
                continue
            cnt += 1
            self.mat[_r][_c].make_bomb()
            for nr,nc in self.neighbors(_r,_c):
                self.mat[nr][nc].increment_adjacency_count()
            
    def click(self, r, c):
        if self.mat[r][c].is_visible():
            return True
        self.mat[r][c].flip()
        if self.mat[r][c].is_bomb():
            self.status = Minesweeper.LOST
            return False
        if self.mat[r][c].adjacent_bombs == 0:
            self.dfs_traverse(r,c)
        return True

    def dfs_traverse(self, r, c):
        stack = [(r,c)]
        while stack:
            c_r, c_c = stack.pop()
            for n_r, n_c in self.neighbors(c_r,c_c):
                if not self.mat[n_r][n_c].is_visible() and self.mat[n_r][n_c].adjacent_bombs() == 0:
                    self.mat[n_r][n_c].flip()
                    stack.append((n_r,n_c))

    def right_click(self, r, c):
        if not self.mat[r][c].is_visible():
            if self.mat[r][c].is_marked():
                self.bombs_rem += 1
                self.mat[r][c].unmark()
            else:
                self.bombs_rem -= 1
                self.mat[r][c].mark()