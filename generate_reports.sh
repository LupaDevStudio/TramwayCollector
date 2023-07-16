pytest .
pylint . | pylint_report > reports/linting/report.html
pylint tools --import-graph="reports/linting/tools.png"
pylint screens --import-graph="reports/linting/screens.png"