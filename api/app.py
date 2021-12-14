from flask import Flask, render_template, request
from sudoku import build_vanilla_region_map
from models import *


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
        chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        models_selected = request.form.get('comp_select1')
        l_rules_from_model = request.form.getlist('comp_select2')
        get_dim_generation = request.form.get('dim_sudoku')
        sudoku = build_sudoku(models_selected, build_vanilla_region_map(dim=int(get_dim_generation)), l_rules_from_model)
        grid_solved = sudoku.solution
        grid = sudoku.grid
        return render_template("new_sudoku.html",
                               grid_solved=grid_solved,
                               grid=grid,
                               chars=chars)


if __name__ == '__main__':
    app.run()
