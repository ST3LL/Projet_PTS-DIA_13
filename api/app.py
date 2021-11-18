import random

import pandas as pd
from flask import Flask, render_template, request
from sudoku import Game, build_vanilla_region_map

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home_app():
    return render_template('home.html')


@app.route('/generate_solution/', methods=['GET', 'POST'])
def GenerateSolution():
    game = Game(build_vanilla_region_map())
    grid = game.solution
    return render_template('generate_solution.html',
                           grid=grid)


@app.route("/new_sudoku/", methods=['GET', 'POST'])
def NewSudoku():
    game = Game(build_vanilla_region_map())
    grid_solved = game.solution
    grid = game.grid
    print(grid_solved)
    return render_template("new_sudoku.html",
                           grid_solved=grid_solved,
                           grid=grid)


if __name__ == '__main__':
    app.run()
