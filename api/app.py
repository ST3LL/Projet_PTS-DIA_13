from random import shuffle

from flask import Flask, render_template, request
from utils import build_vanilla_region_map, get_color_list, EMPTY
from pts_main import build_sudoku, get_models_and_rules
from math import sqrt


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return "A dimension is an integer."


@app.route('/', methods=['GET', 'POST'])
def home_app():
    return render_template('home.html', models=get_models_and_rules())


@app.route("/new_sudoku/", methods=['GET', 'POST'])
def Sudoku():
    if request.method == 'POST':
        models_selected = request.form.get('comp_select1')
        l_rules_from_model = request.form.getlist('comp_select2')
        hidden_table = request.form.get('hidden_table')
        get_dim_generation = int(request.form.get('dim_sudoku')) if request.form.get('dim_sudoku') != '' else 3

        if hidden_table:
            tab = hidden_table.split(',')
            tab = [int(val) - 1 for val in tab]
            region_map = [[tab[i+j*get_dim_generation*get_dim_generation] for i in range(get_dim_generation*get_dim_generation)] for j in range(get_dim_generation*get_dim_generation)]
        else:
            region_map = build_vanilla_region_map(get_dim_generation)
        sudoku = build_sudoku(models_selected,
                              region_map,
                              l_rules_from_model)
        chars = list(sudoku.moveset)
        grid_solved = sudoku.solution
        move_history = sudoku.move_history
        grid = sudoku.grid
        hints = sum([len([x for x in row if x is not None and x != EMPTY]) for row in grid])
        colors = get_color_list()
        return render_template("new_sudoku.html",
                               grid_solved=grid_solved,
                               grid=grid,
                               chars=chars,
                               region_map=sudoku.region_map,
                               colors=colors,
                               sqrt=int(sqrt(len(chars))),
                               move_history=move_history,
                               hints=hints)


@app.route("/region_map/", methods=['GET', 'POST'])
def RegionMap():
    if request.method == 'POST':
        dim = int(request.form.get('dim_region_map')) if request.form.get('dim_region_map') != '' else 3
        full_dim = dim * dim
        chars = list(range(1, full_dim + 1))
        grid = [[1+(j//dim)+(i//dim)+(dim-1)*(j//dim) for i in range(full_dim)] for j in range(full_dim)]
        colors = ['#ffffff' for _ in range(30)]
        return render_template("region_map.html",
                               grid=grid,
                               chars=chars,
                               region_map=grid,
                               colors=colors,
                               sqrt=int(sqrt(len(chars))),
                               models=get_models_and_rules(),
                               dim=dim)


if __name__ == '__main__':
    app.run()
