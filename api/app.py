from flask import Flask, render_template, request
from utils import build_vanilla_region_map
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
        get_dim_generation = request.form.get('dim_sudoku')
        sudoku = build_sudoku(models_selected,
                              build_vanilla_region_map(dim=int(get_dim_generation)),
                              l_rules_from_model)
        chars = list(sudoku.moveset)
        grid_solved = sudoku.solution
        grid = sudoku.grid
        colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffa500', '#00ffa5', '#a500ff']
        return render_template("new_sudoku.html",
                               grid_solved=grid_solved,
                               grid=grid,
                               chars=chars,
                               region_map=sudoku.region_map,
                               colors=colors,
                               sqrt=int(sqrt(len(chars))))


if __name__ == '__main__':
    app.run()
