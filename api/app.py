import pandas as pd
from flask import Flask, render_template, request
from sudoku import generate_full_grid

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home_app():
    return render_template('home.html')


@app.route('/generate_solution/', methods=['GET', 'POST'])
def GenerateSolution():
    grid = generate_full_grid()
    df_grid = pd.DataFrame(grid)
    return render_template('generate_solution.html',
                           output_data=[df_grid.to_html(classes='d')])


@app.route("/new_sudoku/", methods=['GET', 'POST'])
def NewSudoku():
    return render_template("new_sudoku.html")


if __name__ == '__main__':
    app.run()
