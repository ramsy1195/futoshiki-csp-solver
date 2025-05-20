# Futoshiki Puzzle Solver

A Python-based solver for the Futoshiki puzzle, a logic puzzle similar to Sudoku with added inequality constraints between cells. This solver uses backtracking with forward checking and the Minimum Remaining Values (MRV) heuristic for efficient constraint satisfaction.

## What is Futoshiki?

Futoshiki is a grid-based puzzle where you must:
- Fill each cell with numbers from 1 to N (N × N grid).
- Ensure all numbers in each row and column are unique.
- Satisfy inequality constraints (e.g., a cell must be greater than or less than its neighbor).

## Features

- Supports any `N x N` Futoshiki puzzle (default is 5x5).
- Enforces:
  - Row and column uniqueness.
  - Inequality constraints.
- Uses:
  - Backtracking algorithm.
  - Forward checking to prune inconsistent values.
  - Minimum Remaining Values (MRV) heuristic for variable ordering.

## Project Structure

```text
.
├── futoshiki.py  # Main Python file
└── README.md  
```

## Requirements

- Python 3.x
- No external dependencies

## Usage
1. Input Format:
- Store unsolved Futoshiki puzzles in `start.txt`, one puzzle per line.
- Each puzzle is a single-line string encoding the grid from top-left to bottom-right.
- Numbers (`0` for empty), dashes (`-`) for no constraint, and `<`, `>`, `^`, `v` for inequalities.
- Horizontal constraints are between numbers, vertical constraints come after each row.
- Example: ```0-0<0---0<2-0<--0-0-0``` corresponds to the following 4x4 grid:

  
  ```
  0   0 < 0
              
  0 < 2   0
  ^              
  0   0   0
  ```
2. Run the Solver:
```bash
python futoshiki_solver.py
```
3. Output:
- Solutions are saved to `output.txt`, one solved puzzle per line, using the same string format.

## Notes

- The puzzle encoding uses a compact linear string format that interleaves cell values with inequality constraints, enabling easy parsing and serialization.
- The solver leverages backtracking enhanced with forward checking and the Minimum Remaining Values (MRV) heuristic to prune the search space and improve efficiency.
- This approach guarantees that all puzzles with a unique solution can be solved without exhaustive brute force.
- Inequality constraints between adjacent cells are carefully handled both horizontally and vertically, preserving the puzzle logic during search.
- Possible extensions include:
  - Incorporating more advanced constraint propagation techniques such as Arc Consistency (AC-3) or Constraint Learning.
  - Supporting larger board sizes or non-square Futoshiki variants.
  - Developing a user-friendly GUI or web interface for interactive puzzle creation and solution visualization.
  - Adding parallel processing to speed up solving time for batch puzzle solving.
