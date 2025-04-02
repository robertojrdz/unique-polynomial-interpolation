from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve/<int:n>', methods=['POST'])
def solve(n: int):
    x = []
    sorted_x = []
    y = []
    for i in range(n):
        x.append(float(request.form[f'x_{i}']))
        sorted_x.append(float(request.form[f'x_{i}']))
        y.append(float(request.form[f'y_{i}']))
    x_n = float(request.form['x_n'])
    sorted_x.sort()
    if x == sorted_x:
        if x_n <= x[n-1]:
            if x_n >= x[0]:
                matrix = np.zeros((n, n+1))
                for row in range(n):
                    matrix[row, 0] = 1
                for row in range(n):
                    for col in range(n):
                        if col != 0:
                            matrix[row, col] = x[row]**col
                for row in range(n):
                    matrix[row, n] = y[row]
                a = []
                for item in gauss_jordan(n, matrix):
                    a.append(float(item))
                print(f"a = {a}")
                p_n = 0.0
                for i in range(n):
                    p_n += a[i]*(x_n**i)
                print(f"p({x_n}) = {p_n}")
            else:
                return render_template('index.html', error = '!inside')
        else:
            return render_template('index.html', error = '!inside')
    else:
        return render_template('index.html', error = '!sort')
    return render_template("solution.html", p_n = p_n, x_n = x_n, a = a, x = x, y = y)

def gauss_jordan(n, matrix):
    solution = []
    for h in range(n):
        if matrix[h, h] == 0:
            max_row = h + np.argmax(np.abs(matrix[h:, h]))
            if matrix[max_row, h] == 0:
                raise Exception("No solution")
            matrix[[h, max_row]] = matrix[[max_row, h]]
        x = matrix[h, h]
        for i in range(n+1):
            matrix[h, i] /= x
        y = []
        for i in range(n):
            y.append(matrix[i, h])
        for i in range(n):
            for j in range(n+1):
                if h != i:
                    matrix[i, j] = (matrix[h, j] * (-y[i])) + matrix[i, j]
    for i in range(n):
        solution.append(matrix[i, n])
    return solution

if __name__ == '__main__':
    app.run(debug=True)