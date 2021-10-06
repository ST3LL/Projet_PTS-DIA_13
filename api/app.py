import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home_app():
    return render_template('home.html')


@app.route('/result/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        select_nb_rows = request.form.get('comp_select_nb_rows')
        select_nb_columns = request.form.get('comp_select_nb_cols')
        grids = []
        for _ in range(int(select_nb_rows) + 1):
            grids.append(["*"] * int(select_nb_columns))
        df_grids = pd.DataFrame(grids)
        return render_template('result.html',
                               output_data=[df_grids.to_html(classes='d')],
                               size_cols=int(select_nb_columns),
                               size_rows=int(select_nb_rows))


if __name__ == '__main__':
    app.run()
