from flask import Flask, render_template, request, redirect, url_for

from model import task_DAL as db

from datetime import datetime

app = Flask(__name__,
            template_folder='view/templates',
            static_folder='view/static')


@app.route('/', methods=['GET'])
def index():
    class_key = request.args.get('class_key')
    classes = db.get_classes()

    if class_key is None or class_key not in classes:
        class_key = classes[0]
        return redirect(url_for('index', class_key=class_key))

    task_list = db.get_tasks_for_class(get_class_id(class_key))

    return render_template('index.html',
                           classes=classes,
                           class_key=class_key,
                           task_list=task_list)

@app.route('/add_task_form', methods=['POST'])
def add_task_form():
    classes = db.get_classes()
    return render_template('add_task.html', classes=classes)

@app.route('/add_task', methods=['POST'])
def add_task():
    class_name = request.form.get('class_name')
    task_name = request.form.get('task_name')
    due_date = request.form.get('due_date')

    if class_name is None or class_name == "" or task_name is None or task_name == "" or due_date is None or due_date == "":
        return render_template('error.html', message="All fields are required to add a task.")

    if due_date is not None:
        try:
            date1 = datetime.strptime("2024-03-15", "%Y-%m-%d")
            date2 = datetime.strptime("2024-04-01", "%Y-%m-%d")
            if date1 < date2:
                return render_template('error.html', message="Due date cannot be in the past.")

        except ValueError:
            return render_template('error.html', message="Invalid date format. Please use YYYY-MM-DD.")

    class_id = get_class_id(class_name)

    if class_id is None:
        return render_template('error.html',message="Invalid class.")

    db.add_task(class_id, task_name, due_date)
    return redirect(url_for('index', class_key=class_name))


@app.route('/remove_task', methods=['POST'])
def remove_task():
    class_key = request.form.get('class_id')
    task_id = request.form.get('task_id')
    db.delete_task(task_id)
    return redirect(url_for('index', class_id=class_key))

def get_class_id(class_name):
    return db.get_class_id(class_name)

if __name__ == '__main__':
    app.run()
