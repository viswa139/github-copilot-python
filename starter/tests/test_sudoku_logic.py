import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "sudoku_logic.py"

spec = importlib.util.spec_from_file_location("sudoku_logic", MODULE_PATH)
sudoku_logic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sudoku_logic)


def test_create_empty_board_has_correct_size_and_defaults():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_is_safe_rejects_conflicts_in_row_column_and_box():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.is_safe(board, 0, 0, 1) is True

    board[0][1] = 1
    assert sudoku_logic.is_safe(board, 0, 0, 1) is False

    board = sudoku_logic.create_empty_board()
    board[1][0] = 1
    assert sudoku_logic.is_safe(board, 0, 0, 1) is False

    board = sudoku_logic.create_empty_board()
    board[1][1] = 1
    assert sudoku_logic.is_safe(board, 0, 0, 1) is False


def test_deep_copy_returns_independent_board_copy():
    board = [[1, 2], [3, 4]]
    copied = sudoku_logic.deep_copy(board)

    copied[0][0] = 9

    assert board[0][0] == 1
    assert copied[0][0] == 9


def test_remove_cells_reduces_number_of_clues():
    board = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
    ]

    sudoku_logic.remove_cells(board, 40)

    clues = sum(cell != sudoku_logic.EMPTY for row in board for cell in row)
    assert clues == 40


def test_generate_puzzle_respects_difficulty_levels():
    easy_puzzle, _ = sudoku_logic.generate_puzzle(difficulty="easy")
    medium_puzzle, _ = sudoku_logic.generate_puzzle(difficulty="medium")
    hard_puzzle, _ = sudoku_logic.generate_puzzle(difficulty="hard")

    easy_clues = sum(cell != sudoku_logic.EMPTY for row in easy_puzzle for cell in row)
    medium_clues = sum(cell != sudoku_logic.EMPTY for row in medium_puzzle for cell in row)
    hard_clues = sum(cell != sudoku_logic.EMPTY for row in hard_puzzle for cell in row)

    assert easy_clues > medium_clues > hard_clues
