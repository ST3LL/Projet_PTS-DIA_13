from flask import Flask, render_template, request
from sudoku import build_vanilla_region_map
from models import *
from flask_wtf import FlaskForm
from wtforms import SelectField


app = Flask(__name__)


class Form(FlaskForm):
    models = SelectField('models', choices=get_models_and_rules().keys())
    rules_from_models = SelectField('rules', choices=[])


@app.errorhandler(404)
def page_not_found(e):
    return "A dimension is an integer."


@app.route('/', methods=['GET', 'POST'])
def home_app():
    form = Form()
    form.rules_from_models.choices = [get_models_and_rules()[m] for m in get_models_and_rules().keys()]
    if request.method == 'POST':
        return

    return render_template('home.html', form=form, models=get_models_and_rules())


@app.route('/generate_solution/', methods=['GET', 'POST'])
def GenerateSolution():
    if request.method == 'POST':
        models_selected = request.form.get('comp_select1')
        print(models_selected)
        get_dim_generation = request.form.get('dim_sudoku_generation')
        print(get_dim_generation)
        sudoku = build_sudoku(models_selected, build_vanilla_region_map(dim=int(get_dim_generation)), ['rule_row', 'rule_col', 'rule_region'])
        sol = sudoku.solution
        return render_template('generate_solution.html', grid=sol)


@app.route("/new_sudoku/", methods=['GET', 'POST'])
def NewSudoku():
    if request.method == 'POST':
        chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        models_selected = request.form.get('comp_select2')
        get_dim_generation = request.form.get('dim_sudoku')
        sudoku = build_sudoku(models_selected, build_vanilla_region_map(dim=int(get_dim_generation)), ['rule_row', 'rule_col', 'rule_region'])
        grid_solved = sudoku.solution
        grid = sudoku.grid
        print(grid)
        return render_template("new_sudoku.html",
                               grid_solved=grid_solved,
                               grid=grid,
                               chars=chars)


if __name__ == '__main__':
    app.run()
