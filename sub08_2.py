import tkinter as tk
from tkinter import messagebox
import sqlite3

# データベースのセットアップ
conn = sqlite3.connect('todo2.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY, task TEXT, status TEXT)''')
conn.commit()

# タスクを追加する関数
def add_task():
    task = task_entry.get()
    if task:
        c.execute('INSERT INTO tasks (task, status) VALUES (?, ?)', (task, '未完了'))
        conn.commit()
        task_entry.delete(0, tk.END)
        display_tasks()
    else:
        messagebox.showwarning("警告", "タスクを入力してください")

# タスクを完了にする関数
def complete_task():
    try:
        task_id = task_listbox.get(task_listbox.curselection())[0]
        c.execute('UPDATE tasks SET status = ? WHERE id = ?', ('完了', task_id))
        conn.commit()
        display_tasks()
    except:
        messagebox.showwarning("警告", "タスクを選択してください")

# タスクを表示する関数
def display_tasks():
    task_listbox.delete(0, tk.END)
    for row in c.execute('SELECT * FROM tasks'):
        task_listbox.insert(tk.END, row)

# GUIのセットアップ
root = tk.Tk()
root.title("ToDoリスト")

task_entry = tk.Entry(root, width=50)
task_entry.pack(pady=10)

add_button = tk.Button(root, text="タスクを追加", command=add_task)
add_button.pack(pady=5)

complete_button = tk.Button(root, text="タスクを完了", command=complete_task)
complete_button.pack(pady=5)

task_listbox = tk.Listbox(root, width=50, height=15)
task_listbox.pack(pady=10)

display_tasks()

root.mainloop()

# アプリケーション終了時にデータベース接続を閉じる
conn.close()
