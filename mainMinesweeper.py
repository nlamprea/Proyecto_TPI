import os
from programExecutionMinesweeper import run_program

def main():
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    run_program(ruta_base)
