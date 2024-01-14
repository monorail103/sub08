import tkinter as tk
from tkinter import ttk

root = tk.Tk()
treeView = ttk.Treeview(root)
treeView.pack(fill=tk.BOTH)

## リストとして使うための準備
treeView.config(
    show="", # ヘッダーとツリー用アイコン領域を非表示
    columns=["label", "value"], # 任意の column を設定可能
    displaycolumns=["label"], # 表示用に使う column を指定
    selectmode="browse", # 複数選択の禁止
)

## Sample Data
treeView.insert("", "end", values=("1月", "jan"))
treeView.insert("", "end", values=("2月", "feb"))
treeView.insert("", "end", values=("3月", "mar"))

def onTreeSelectedMulti(event):
    # 複数選択の場合は、forループで処理
    view = event.widget
    for idx in view.selection():
        label, value = view.item(idx, "values")
        print(">", label, value)

def onTreeSelectedSingle(event):
    # 単一選択の場合は現在のアクティブな行のみ
    view = event.widget
    label, value = view.item(view.focus(), "values")
    print(">", label, value)

# treeView.bind("<<TreeviewSelect>>", onTreeSelectedMulti)
treeView.bind("<<TreeviewSelect>>", onTreeSelectedSingle)

root.mainloop()