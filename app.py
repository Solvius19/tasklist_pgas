from flask import Flask, render_template, request

import task_DAL as db

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task_name = request.form.get('class_id')
        task_name = request.form.get('task_name')
        task_name = request.form.get('due_date')


if __name__ == '__main__':
    app.run()
