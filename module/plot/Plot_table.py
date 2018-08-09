# TIPSY: Telco pIPeline benchmarking SYstem
#
# Copyright (C) 2018 by its authors (See AUTHORS)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import inspect

from Plot_simple import Plot as Plot_base
from Plot_simple import str2tex

class Plot(Plot_base):
    def __init__(self, conf):
        super().__init__(conf)
        self.preamble += inspect.cleandoc(r"""
          \usepackage{pgfplotstable}
          \usepackage{colortbl}
        """) + "\n"

    def format_latex(self, series, title):
        f = {'title': title, 'plot_args': '', 'addplot': ''}

        names = [self.conf.x_axis] + [s[0] for s in series.items()]
        names = [str2tex(n) for n in names]
        f['header'] = ' & '.join(names)

        x_vals = []
        for s in series.items():
            x_vals += list(zip(*s[1]))[0]
        x_vals = sorted(set(x_vals))

        sdict = [{k: v for k, v in points} for points in series.values()]
        if len(x_vals) != 1:
            for x in x_vals:
                vals = [str(x)]
                for s in sdict:
                    vals.append(str(s.get(x, 'nan')))
                f['addplot'] += ' & '.join(vals) + "\\\\ \n    "
        else:
            f['plot_args'] = 'string type,column type=l,'
            f['header'] = 'variable & value'
            x = x_vals[0]
            line = "%s & %s\\\\ \n    "
            f['addplot'] += line % (self.conf.x_axis, x)
            for var in self.conf.y_axis:
                print(var, series[var])
                val = series[var][0][1]
                f['addplot'] += line % (str2tex(var), val)

        text = inspect.cleandoc(r"""
          \begin{{table}}
            \tiny
            \centering
            \caption{{{title}}}
            \pgfplotstabletypeset[col sep=&,row sep=\\,{plot_args}
              every even row/.style={{before row={{\rowcolor[gray]{{0.9}}}}}}]{{
              {header} \\
              {addplot}}}
          \end{{table}}
          """
        ).format(**f)
        with open('fig.tex', 'w') as f:
            f.write(text)
            f.write("\n")