# Type: 'python3 setyp.py build' in terminal
import cx_Freeze

executables = [cx_Freeze.Executable("GraphicSudoku.py")]

cx_Freeze.setup(
    name="SudokuProject",
    options={"build_exe":{"packages":{"pygame","os","sys","time","random"},"include_files":{"assets","Sudoku.py"}}},
    description="Sudoku Project by JaviBT",
    executables = executables
)
