from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'XXXXXXXXXXX'
db_name = "tasks.db"

# Criação do banco de dados e tabela
def create_db():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 description TEXT,
                 completed INTEGER)''')
    conn.commit()
    conn.close()

# Rota para exibir todas as tarefas
@app.route('/')
def index():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Rota para adicionar uma nova tarefa
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
              (title, description, 0))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Rota para editar uma tarefa
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        completed = 1 if 'completed' in request.form else 0
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("UPDATE tasks SET title=?, description=?, completed=? WHERE id=?",
                  (title, description, completed, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        task = c.fetchone()
        conn.close()
        return render_template('edit.html', task=task)

# Rota para concluir uma tarefa
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    flash('Tarefa marcada como concluída', 'success')
    return redirect(url_for('index'))

# Rota para excluir uma tarefa
@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_db()
    app.run(debug=True)