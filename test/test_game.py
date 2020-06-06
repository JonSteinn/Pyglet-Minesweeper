
from random import uniform
from minesweeper.game import Minesweeper, MinesweeperSquare


def test_msquare_init_default():
    mss = MinesweeperSquare()
    assert not mss.is_visible()
    assert not mss.is_bomb()
    assert not mss.is_marked()

def test_msquare_init():
    mss = MinesweeperSquare(-1, True, False)
    assert mss.is_bomb()
    assert mss.is_visible()
    assert not mss.is_marked()

def test_msquare_flip():
    mss = MinesweeperSquare()
    assert not mss.is_visible()
    mss.flip()
    assert mss.is_visible()
    mss.flip()
    assert not mss.is_visible()

def test_msquare_bomb():
    mss = MinesweeperSquare()
    assert not mss.is_bomb()
    mss.make_bomb()
    assert mss.is_bomb()
    mss.make_bomb()
    assert mss.is_bomb()

def test_msquare_adjacency():
    mss = MinesweeperSquare()
    mss.increment_adjacency_count()
    mss.increment_adjacency_count()
    mss.increment_adjacency_count()
    assert mss.adjacent_bombs() == 3

def test_msquare_mark():
    mss = MinesweeperSquare()
    assert not mss.is_marked()
    mss.mark()
    assert mss.is_marked()
    mss.mark()
    assert mss.is_marked()
    mss.unmark()
    assert not mss.is_marked()
    mss.unmark()
    assert not mss.is_marked()

def test_ms_init():
    for _ in range(5):
        for r in range(Minesweeper.ROW_SIZE):
            for c in range(Minesweeper.COL_SIZE):
                ms = Minesweeper(r, c)
                assert not ms.is_over()
                assert not ms.is_won()
                assert not ms.mat[r][c].is_bomb()
                assert ms.mat[r][c].is_visible()

def test_ms_init_empty():
    r, c = int(uniform(0, Minesweeper.ROW_SIZE)), int(uniform(0, Minesweeper.COL_SIZE))
    while True:
        ms = Minesweeper(r,c)
        if ms.mat[r][c].adjacent_bombs() == 0:
            break
    for n_r, n_c in Minesweeper._neighbors(r, c):
        assert not ms.mat[n_r][n_c].is_bomb()

    for _r in range(Minesweeper.ROW_SIZE):
        for _c in range(Minesweeper.COL_SIZE):
            if ms.mat[_r][_c].is_bomb():
                assert not ms.mat[_r][_c].is_visible()

def test_ms_init_adjacent():
    r, c = int(uniform(0, Minesweeper.ROW_SIZE)), int(uniform(0, Minesweeper.COL_SIZE))
    while True:
        ms = Minesweeper(r,c)
        if ms.mat[r][c].adjacent_bombs() > 0:
            break

    ab = sum(ms.mat[n_r][n_c].is_bomb() for n_r, n_c in Minesweeper._neighbors(r, c))
    assert ab == ms.mat[r][c].adjacent_bombs()

    visible = 0
    for _r in range(Minesweeper.ROW_SIZE):
        for _c in range(Minesweeper.COL_SIZE):
            if ms.mat[_r][_c].is_visible():
                visible += 1
    assert visible == 1

def test_ms_neighbors():
    ms = Minesweeper(5,5)
    assert {x for x in Minesweeper._neighbors(0,0)} == {(0,1), (1,0), (1,1)}
    assert {x for x in Minesweeper._neighbors(4,0)} == {(3,0),(5,0),(3,1),(5,1),(4,1)}
    assert {x for x in Minesweeper._neighbors(15,15)} == {(15,14),(14,15),(14,14)}
    assert {x for x in Minesweeper._neighbors(5,5)} == {(4,4),(5,4),(6,4),(4,5),(6,5),(4,6),(5,6),(6,6)}

def test_ms_adjacent_numbers():
    ms = Minesweeper(5,5)
    for i in range(16):
        for j in range(16):
            ab = ms.mat[i][j].adjacent_bombs()
            if ab != -1:
                assert ab == sum(1 for a,b in Minesweeper._neighbors(i,j) if ms.mat[a][b].is_bomb())

