"""The game logic for minesweeper, independent of UI.
"""

from random import uniform
from typing import List, Iterator, Tuple

class MinesweeperSquare:
    """A single square on the minesweeper board.
    """

    def __init__(self, adjacency_count: int = 0,
                 flipped: bool = False, marked: bool = False) -> None:
        """Create an instance of a Minesweeper square, the state of each square.

        Args:
            adjacency_count (int, optional): How many of the neighboring squares
            are bombs. Defaults to 0.
            flipped (bool, optional): Has this square been revealed by the player.
            Defaults to False.
            marked (bool, optional): Is this square currently marked as a bomb by
            the player. Defaults to False.
        """
        self.adjacency_count: int = adjacency_count
        self.flipped: bool = flipped
        self.marked: bool = marked

    def flip(self) -> None:
        """Make visible if not, and vice versa.
        """
        self.flipped = not self.flipped

    def is_visible(self) -> bool:
        """Check if the squared has been flipped to show adjacency count.

        Returns:
            bool: True iff visible.
        """
        return self.flipped

    def make_bomb(self) -> None:
        """Make the square a bomb.
        """
        self.adjacency_count = -1

    def is_bomb(self) -> bool:
        """Check if the square is a bomb.

        Returns:
            bool: True iff bomb.
        """
        return self.adjacency_count == -1

    def increment_adjacency_count(self) -> None:
        """Increase the adjacency count by one.
        """
        self.adjacency_count += 1

    def adjacent_bombs(self) -> int:
        """How many of the NW,N,NE,E,SE,S,SW,W squares (if they exist)
        are bombs?

        Returns:
            int: The number of bombs adjacent to this square.
        """
        return self.adjacency_count

    def mark(self) -> None:
        """Mark the square as a potential bomb.
        """
        self.marked = True

    def unmark(self) -> None:
        """Remove a mark from the square.
        """
        self.marked = False

    def is_marked(self) -> bool:
        """Check if square has a mark.

        Returns:
            bool: True iff marked.
        """
        return self.marked

class Minesweeper:
    """The actual game to be played. It supports two operations, left nad
    right clicking and the state of the game can also be checked.
    """

    # The number of rows
    ROW_SIZE: int = 16
    # The number of columns
    COL_SIZE: int = 16
    # The number of bombs
    TOTAL_BOMBS: int = 40
    # Enum for game states
    WON, LOST, ONGOING = range(3)

    def __init__(self, r: int, c: int) -> None:
        """Create an instance of a minesweeper game and generate the bombs
        so that (r,c) won't have one, then simulate (r,c) being left clicked.

        Args:
            r (int): The row of the click.
            c (int): The column of the click.
        """
        self.mat: List[List[MinesweeperSquare]] = [
            [MinesweeperSquare() for _ in range(Minesweeper.COL_SIZE)]
            for _ in range(Minesweeper.ROW_SIZE)
        ]
        self.unflipped = Minesweeper.ROW_SIZE * Minesweeper.COL_SIZE
        self._generate(r, c)
        self.state: int = Minesweeper.ONGOING
        self.bombs_rem: int = Minesweeper.TOTAL_BOMBS
        self.left_click(r, c)

    def left_click(self, r: int, c: int) -> bool:
        """Left click to reveal a square.

        Args:
            r (int): The row of the click.
            c (int): The column of the click.

        Returns:
            bool: True if any change was made.
        """

        if self.state != Minesweeper.ONGOING:
            return False

        if self.mat[r][c].is_visible():
            return False

        self.mat[r][c].flip()
        self.unflipped -= 1

        if self.mat[r][c].is_bomb():
            self.state = Minesweeper.LOST
            return True

        if self.mat[r][c].adjacent_bombs() == 0:
            self._dfs_traverse(r, c)

        if self.unflipped == 0:
            self.state = Minesweeper.WON

        return True

    def right_click(self, r: int, c: int) -> None:
        """Place a mark to indicate that a bomb is believed to be
        present at this place.

        Args:
            r (int): The row of the click.
            c (int): The column of the click.
        """
        if not self.mat[r][c].is_visible():
            if self.mat[r][c].is_marked():
                self.bombs_rem += 1
                self.mat[r][c].unmark()
            elif self.bombs_rem > 0:
                self.bombs_rem -= 1
                self.mat[r][c].mark()

    def is_over(self) -> bool:
        """Check if game is over.

        Returns:
            bool: True iff won or lost.
        """
        return self.state != Minesweeper.ONGOING

    def is_won(self) -> bool:
        """Check if game is won.

        Returns:
            bool: True iff won.
        """
        return self.state == Minesweeper.WON

    def _neighbors(self, r: int, c: int) -> Iterator[Tuple[int, int]]:
        """Generate all adjacent positions of (r,c).

        Args:
            r (int): The row of the click.
            c (int): The column of the click.

        Yields:
            (int,int): The row-col coordinate of a neighbor.
        """
        for _r, _c in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            if 0 <= r + _r < Minesweeper.ROW_SIZE and \
                0 <= c + _c < Minesweeper.COL_SIZE:
                yield r+_r, c+_c

    def _generate(self, r: int, c: int) -> None:
        """Randomly generate the board so that (r,c) does not
        contain a bomb and that bomb count is reached.

        Args:
            r (int): The row of the click.
            c (int): The column of the click.
        """
        cnt = 0
        while cnt < Minesweeper.TOTAL_BOMBS:
            _r = int(uniform(0, Minesweeper.ROW_SIZE))
            _c = int(uniform(0, Minesweeper.COL_SIZE))
            if (_r == r and _c == c) or self.mat[_r][_c].is_bomb():
                continue
            cnt += 1
            self.mat[_r][_c].make_bomb()
            for n_r, n_c in self._neighbors(_r, _c):
                if not self.mat[n_r][n_c].is_bomb():
                    self.mat[n_r][n_c].increment_adjacency_count()

    def _dfs_traverse(self, r: int, c: int) -> None:
        """Traverse the board of no-neighbor-squares and flip
        all in its path.

        Args:
            r (int): The row of the click.
            c (int): The column of the click.
        """
        stack = [(r, c)]
        while stack:
            c_r, c_c = stack.pop()
            for n_r, n_c in self._neighbors(c_r, c_c):
                if not self.mat[n_r][n_c].is_visible():
                    if self.mat[n_r][n_c].adjacent_bombs() >= 0:
                        self.mat[n_r][n_c].flip()
                        if self.mat[n_r][n_c].adjacent_bombs() == 0:
                            stack.append((n_r, n_c))
