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
                           '\\geometry{hmargin=1.5cm, vmargin=2cm}',
                           '\\usepackage{multicol}',
                           '\\setlength{\\columnsep}{6cm}']
        self.function_img = """
        \\newcommand{\\img}[3]{ %scale,lien,description
        \\begin{figure}[!h]
        \\begin{center}
            \\includegraphics[scale=#1]{#2}
            \\caption{#3}
        \\end{center}
        \\end{figure}
        }
        """

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
        self.file.write('\\center{' + element + '}\n')

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
        self.file.write('\\center{\\includegraphics[scale=' + str(scale) + ']{' + path + '}}\n')

    def begin_itemize(self):
        self.file.write('\\begin{itemize}\n')

    def item(self, content: str):
        self.file.write('   \\item ' + content + '\n')

    def end_itemize(self):
        self.file.write('\\end{itemize}\n')

    def color_box_with_title(self, frame_color: str, backgroung_color: str, title: str, content: str):
        self.file.write(
            '\\begin{tcolorbox}[colback=' + backgroung_color + '!5,colframe=' + frame_color + '!40!black,title=' + title + ']\n')
        self.file.write(content + '\n')
        self.file.write('\\end{tcolorbox}\n')

    def color_box(self, frame_color: str, backgroung_color: str, content: str):
        self.file.write(
            '\\begin{tcolorbox}[colback=' + backgroung_color + '!5,colframe=' + frame_color + '!40!black]\n')
        self.file.write(content + '\n')
        self.file.write('\\end{tcolorbox}\n')

    def href(self, link: str, content: str):
        return '\\href{' + link + '}{' + content + '}'

    def bold(self, content: str):
        return '\\textbf{' + content + '}'

    def italic(self, content):
        return '\\textit{' + content + '}'

    def underline(self, content):
        return '\\underline{' + content + '}'

    def text_color(self, color: str, content: str):
        return '\\textcolor{' + color + '}{' + content + '}'

    def newpage(self):
        self.file.write('\\newpage\n')
