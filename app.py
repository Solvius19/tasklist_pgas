from flask import Flask, render_template, request, redirect, url_for

from model import task_DAL as db

app = Flask(__name__)


@app.route('/', args=['GET'])
def index():
    class_key = request.args.get('class_key')
    classes = db.get_classes()

    if class_key is None or class_key not in classes:
        class_key = classes[0]
        return redirect(url_for('index', class_id=class_key))

    task_list = db.get_tasks_for_class(class_key)

    return render_template('index.html',
                           classes=classes,
                           task_list=task_list)

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task_class = request.form.get('class_id')
        task_name = request.form.get('task_name')
        task_date = request.form.get('due_date')
        return render_template('add_task.html', task_class=task_class, task_name=task_name, task_date=task_date)
    return render_template('index.html')

@app.route('/remove_task', methods=['POST'])
def remove_task():
    class_key = request.form.get('class_id')
    task_id = request.form.get('task_id')
    db.delete_task(class_key, task_id)
    return redirect(url_for('index', class_id=class_key))

if __name__ == '__main__':
    app.run()
