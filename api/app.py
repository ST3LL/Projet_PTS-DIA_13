from flask import Flask, render_template, request, redirect
from sudoku import Game, build_vanilla_region_map

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return "A dimension is an integer."


@app.route('/', methods=['GET', 'POST'])
def home_app():
    return render_template('home.html')


@app.route('/generate_solution/', methods=['GET', 'POST'])
def GenerateSolution():
    if request.method == 'POST':
        get_dim = request.form.get('dim_sudoku')
        if not isinstance(get_dim, int):
            return redirect('/404')
        else:
            game = Game(build_vanilla_region_map(dim=get_dim))
            grid_solved = game.solution
    return render_template('generate_solution.html', grid_solved=grid_solved)


@app.route("/new_sudoku/", methods=['GET', 'POST'])
def NewSudoku():
    game = Game(build_vanilla_region_map())
    grid_solved = game.solution
    grid = game.grid
    return render_template("new_sudoku.html", grid_solved=grid_solved, output_data=grid)


if __name__ == '__main__':
    app.run()
