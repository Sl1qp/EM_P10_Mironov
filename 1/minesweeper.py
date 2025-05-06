import dataclasses
from random import sample
from typing import List, Tuple
from xmlrpc.client import FastParser


@dataclasses.dataclass
class Consts:
    moving_neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

class Cell:
    def __init__(self, around_mines: int=0, mine: bool=False):
        self.around_mines: int = around_mines
        self.mine: bool = mine
        self.fl_open: bool = False


def get_cell_icon(cell: Cell) -> str:
    if cell.fl_open:
        if cell.mine:
            return "*"
        return f"{cell.around_mines}"
    return "#"

def get_cell_icon_adm(cell: Cell) -> str:
    if cell.mine:
        return "*"
    return f"{cell.around_mines}"


class GamePole:
    def __init__(self, n: int, m: int):
        self.n: int = n
        self.m: int = m
        self.field: List[List[Cell]] = [[Cell() for _ in range(n)] for _ in range(n)]
        self.__init_filed()

    def __init_filed(self):
        mines_coordinate = sample(range(0, self.n**2), self.m)
        for coord in mines_coordinate:
            x = coord // self.n
            y = coord - x * self.n
            self.field[x][y] =  Cell(around_mines=0, mine=True)
            for row_idx, col_idx in Consts.moving_neighbors:
                row_n_ind = x+row_idx
                col_n_ind = y+col_idx
                if self.is_cell_in_field(row_n_ind, col_n_ind):

                    self.field[row_n_ind][col_n_ind].around_mines += 1

    def is_cell_in_field(self, row_idx: int, col_idx: int) -> bool:
        return 0 <= row_idx < self.n and 0 <= col_idx < self.n

    def show(self):
        for row in self.field:
            print(''.join(f"{get_cell_icon_adm(cell)} " for cell in row))
