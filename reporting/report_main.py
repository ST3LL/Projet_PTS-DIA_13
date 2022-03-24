from report_generator import SudokuReportGenerator
import pandas as pd
import subprocess
import pickle
import re
import os


def avg_list(l_elt: list):
    return sum(l_elt) / len(l_elt)


def var_list(l_elt: list):
    return sum((x - avg_list(l_elt))**2 for x in l_elt) / len(l_elt)


def var_batch(l_elt: list, length_batch: int):
    k = len(l_elt) / length_batch
    assert k.is_integer()
    mtx = [l_elt[i * length_batch: (i+1) * length_batch] for i in range(int(k))]
    l_var = [var_list(sub) for sub in mtx]
    return var_list(l_var)


def separating_df(df: pd.DataFrame):
    d_df = {m: [df.loc[:, ['dimension', 'difficulty', 'average time', 'average time variance',
                           'variance of time variance batches']][df['model'].squeeze().str.contains(m)],
                df.loc[:, ['dimension', 'difficulty', 'average accuracy', 'average accuracy variance',
                           'variance of accuracy variance batches']][df['model'].squeeze().str.contains(m)]]
            for m in df['model'].squeeze().unique().tolist()}
    return d_df


if __name__ == '__main__':
    file_tex = './sudoku_report.tex'
    output = './output/'

    l_files = [entry for entry in os.listdir('../log_pickle/data')]

    cols = ['model', 'dimension', 'difficulty', 'average time', 'average time variance',
            'variance of time variance batches', 'average accuracy', 'average accuracy variance',
            'variance of accuracy variance batches']
    df = pd.DataFrame(columns=[cols])

    for file in l_files:
        l_data_tuples = pickle.load(open(f'../log_pickle/data/{file}', 'rb'))
        l_data_times, l_data_accuracy = [x[0] for x in l_data_tuples], [x[1] for x in l_data_tuples]
        dico = re.search(
            r"(?P<scrap_batch>\w+_\w+)_(?P<model>[\w-]+)_(?P<dim>\d)_(?P<dif>\d+)_(?P<quantity>\d+)_(?P<variations>\d+)",
            file).groupdict()
        l_to_add = [
            dico['model'],
            dico['dim'],
            dico['dif'],
            "{:3e}".format(avg_list(l_data_times)),
            "{:3e}".format(var_list(l_data_times)),
            "{:3e}".format(var_batch(l_data_times, int(dico['variations']) + 1)),
            avg_list(l_data_accuracy),
            var_list(l_data_accuracy),
            var_batch(l_data_accuracy, int(dico['variations']) + 1)
        ]
        df = df.append(pd.DataFrame(data=[l_to_add], columns=[cols]), ignore_index=True)

    df.to_csv('./output/comparaison_table.csv')

    d_df_models = separating_df(df)

    srg = SudokuReportGenerator(file_path=file_tex, output_path=output)
    srg.begin_document('Evaluation of AI-based Sudoku Solvers')
    srg.section('Sudoku solvers dimension/difficulty/time/accuracy comparison')
    for model, df_model in d_df_models.items():
        srg.subsection(f'{model}')
        srg.table(df_model[0])
        srg.table(df_model[1])
        srg.newpage()

    srg.section('Resolution Time Evolution Plot')
    srg.figure(0.4, './reporting/time.png')
    srg.section('Resolution Accuracy Evolution Plot')
    srg.figure(0.4, './reporting/accuracy.png')
    srg.end_document()

    subprocess.run(f'pdflatex -output-directory={output} {file_tex}', shell=True)
