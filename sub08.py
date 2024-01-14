from tkinter import *
from tkinter import ttk
import sqlite3
import datetime
import tkinter.messagebox as messagebox

# データベース処理
db = 'todo.db'
conn = sqlite3.connect(db)
c = conn.cursor()
sql = 'select id, date, content, flag from todo where flag = 0'
allList = c.execute(sql)

# 追加処理
def addList(event):
    task = add.get()
    
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%m月%d日')

    if ( task == '' ):
        return None

    sql = 'insert into todo (date, content, flag) values ("'+ date +'","'+ task +'", 0)'

    c.execute(sql)
    conn.commit()

    sql = 'select id, date, content, flag from todo where content = "'+ task +'" '
    allList = c.execute(sql)

    for row in allList:
        if ( row != '' ):
            tmp = f'{row[2]} 登録日時:{row[1]}'
            ListBox.insert(END, tmp)
            d[tmp] = row[2]

    # ListBox.insert(END, task)

    add.delete(0, END)

# 完了時の処理
def completeToDo(event):
    selectedIndex = ACTIVE

    todoText = d[ListBox.get(selectedIndex)]
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%m月%d日')
    
    ListBox.delete(selectedIndex)
    sql = 'update todo set flag = 1, date = "'+ date +'" where content = "'+ todoText +'" '
    print(sql)

    c.execute(sql)
    conn.commit()

# 完了した項目を表示
def show_did(event):
    def show_root():
        root_new.destroy()
    def delete_all():
        res = messagebox.askokcancel('質問', '全項目を削除しますか？')
        print(res)
        if res:
            sql = 'delete from todo'
            c.execute(sql)
            conn.commit()

            res = messagebox.showinfo(
                title="完了",
                message="リセットが完了しました",
                detail="アプリを終了します")
            if res:
                root_new.destroy()
                root.destroy()


    sql = 'select id, date, content, flag from todo where flag = 1'
    didList = c.execute(sql)
    ## 第二画面 ##
    root_new = Tk()
    root_new.title("過去のToDo")
    root_new.geometry("450x400")
    frameB = Frame(root_new)
    frame3 = Frame(frameB)

    backButton = Button(frame3,text='ToDoリストに戻る',command=show_root)
    aldButton = Button(frame3,text='リセット',command=delete_all)

    EndBox = Listbox(frame3,width=50, height=20)

    for row in didList:
        if ( row != '' ):
            tmp = f'{row[2]} 終了日:{row[1]}'
            EndBox.insert(END, tmp)

    ## 第二画面 終わり ##
    
    ### 配置セクション ###
    backButton.grid(row=1,column=0)
    aldButton.grid(row=2,column=0)
    EndBox.grid(row=0,column=0)

    frame3.grid(row=0,column=0)
    frameB.pack()

    ### 配置セクション　終わり ###

    root_new.mainloop()

### 定義セクション ###
    
root = Tk()
root.title("ToDoList")
root.geometry("500x400")

## 第一画面 ##
frameA = Frame(root)

frame1 = Frame(frameA,bd=2)
frame2 = Frame(frameA,bd=2,padx=5)

add = Entry(frame1)
exp = Label(frame1,text = "追加",font=('MS UI Gothic', 15))
addButton = Button(frame1,text='ToDoリストに追加')
didButton = Button(frame1,text='過去のToDo')

label1 = Label(frame2, text = "ToDo",font=('MS UI Gothic', 20))
ListBox = Listbox(frame2,width=50, height=20)
complete = Button(frame2,text='完了')

complete.bind("<Button-1>", completeToDo)
addButton.bind("<Button-1>", addList)
didButton.bind("<Button-1>", show_did)

## 第一画面 終わり ##

# 見た目と中身相互変換用の辞書
d = {}

for row in allList:
    if ( row != '' ):
        tmp = f'{row[1]} {row[2]}'
        ListBox.insert(END, tmp)
        d[tmp] = row[2]

### 定義セクション 終わり ###

### 配置セクション ###
exp.grid(row=0,column=0,pady=10)
add.grid(row=1,column=0)
addButton.grid(row=2,column=0,pady=10)
didButton.grid(row=3,column=0)

ListBox.grid(row=0,column=0)
complete.grid(row=1,column=0)
label1.grid(row=0,column=0,pady=8)

frame1.grid(row=0,column=1,padx=5)
frame2.grid(row=0,column=0,padx=5)
frameA.pack()

### 配置セクション　終わり ###

root.mainloop()
