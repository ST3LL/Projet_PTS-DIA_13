import pandas as pd


class SudokuReportGenerator:
    def __init__(self, file_path, output_path):
        self.file_path = file_path
        self.output_path = output_path
        self.file = open(self.file_path, 'w')
        self.l_packages = ['\\documentclass{article}',
                           '\\usepackage{hyperref}',
                           '\\usepackage{graphicx}',
                           '\\usepackage{booktabs}',
                           '\\usepackage{hyperref}',
                           '\\usepackage{geometry}',
                           '\\geometry{hmargin=1.5cm, vmargin=2cm}']

    def packages(self):
        for p in self.l_packages:
            self.file.write(p + '\n')

    def begin_document(self, title: str):
        self.packages()
        self.file.write('\\title{' + title + '}\n')
        self.file.write('\\begin{document}\n')
        self.file.write('\\maketitle\n')
        self.file.write('\\date{}\n')

    def end_document(self):
        self.file.write('\\end{document}\n')
        self.file.close()

    def center(self, element: str):
        begin = '\\begin{center}\n'
        end = '\\end{center}\n'
        self.file.write(begin + element + end)

    def section(self, title: str):
        self.file.write('\\section{' + title + '}\n')

    def subsection(self, title: str):
        self.file.write('\\subsection{' + title + '}\n')

    def subsubsection(self, title: str):
        self.file.write('\\subsubsection{' + title + '}\n')

    def paragraph(self, content: str):
        self.file.write('\\noindent\n')
        self.file.write(content + '\n')

    def table(self, df: pd.DataFrame):
        df = df.astype('string')
        df_final = df.to_latex()
        return self.center(df_final)

    def figure(self, scale: float, path: str):
        self.center('\\includegraphics[scale=' + str(scale) + ']{' + path + '}\n')

    def newpage(self):
        self.file.write('\\newpage\n')
