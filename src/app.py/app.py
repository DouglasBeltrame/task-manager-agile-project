from flask import Flask, render_template, request, redirect, url_for
from src.models import Task

app = Flask(__name__)

# Lista em memória para armazenar as tarefas
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_task = Task(title, description)
        tasks.append(new_task)
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = tasks[task_id] if 0 <= task_id < len(tasks) else None
    if task is None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task, task_id=task_id)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)