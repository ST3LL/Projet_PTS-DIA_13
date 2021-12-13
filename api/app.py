from flask import Flask, render_template, request
from sudoku import Game, build_vanilla_region_map
from models import *


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return "A dimension is an integer."


@app.route('/', methods=['GET', 'POST'])
def home_app():
    return render_template('home.html', models=get_models_rules())


@app.route('/generate_solution/', methods=['GET', 'POST'])
def GenerateSolution():
    if request.method == 'POST':
        models_selected = request.form.get('comp')
        print(models_selected)
        l_rules_from_model = get_rules_of_model(models_selected)
        get_dim_generation = request.form.get('dim_sudoku_generation')
        game = build_sudoku('vanilla', build_vanilla_region_map(dim=int(get_dim_generation)), l_rules_from_model)
        # grid = game.solution
        return render_template('generate_solution.html',
                               grid=grid)


@app.route("/new_sudoku/", methods=['GET', 'POST'])
def NewSudoku():
    if request.method == 'POST':
        chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        get_dim = request.form.get('dim_sudoku')
        game = Game(build_vanilla_region_map(dim=int(get_dim)))
        grid_solved = game.solution
        grid = game.grid
        print(grid_solved)
        return render_template("new_sudoku.html",
                               grid_solved=grid_solved,
                               grid=grid,
                               chars=chars)


if __name__ == '__main__':
    app.run()
