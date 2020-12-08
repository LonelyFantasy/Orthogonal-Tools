# encoding: utf-8
# Made By: Lonely_Fantasy💻
# Work Platform: Windows 10 LTSC
from tkinter import *
from tkinter import scrolledtext
from function import *
import os
# ----------需要的全局变量---------- #
result = []  # 存储寻找到的结果，存储detail的地址
input_diction = []  # 输入因素与水平
name = []  # 因素名称保存

# ----------UI部分---------- #
mainwindow = tkinter.Tk()
mainwindow.title('简单正交表查询工具')
mainwindow.iconbitmap('./logo.ico')
mainwindow.resizable(0, 0)  # 禁止窗口大小调整

# 输入水平因素
level = tkinter.StringVar()  # 水平
level.set('2')  # 示例数据
index = tkinter.StringVar()  # 因素
index.set('3')  # 示例数据
Title = Label(mainwindow, text='待查询数据(仅数字)', font=(
    "微软雅黑", 11)).grid(row=0, column=0, sticky=W + E)
Label1 = Label(mainwindow, text='水平', font=(
    "微软雅黑", 11)).grid(row=1, column=0, sticky=W + E)
Label2 = Label(mainwindow, text='因素', font=(
    "微软雅黑", 11)).grid(row=2, column=0, sticky=W + E)
v1 = Entry(mainwindow, textvariable=level)
v1.grid(row=1, column=0, padx=5, pady=5, sticky=W)  # 设置水平输入框显示的位置，以及长和宽属性，请调用level
v2 = Entry(mainwindow, textvariable=index)
v2.grid(row=2, column=0, padx=5, pady=5, sticky=W)  # 设置因素输入框显示的位置，以及长和宽属性，请调用index

# 输入查询结果文本框
Label3 = Label(mainwindow, text='输入窗口', font=(
    "微软雅黑", 11)).grid(row=3, column=0, sticky=W + E)
search1 = scrolledtext.ScrolledText(mainwindow, width=50, height=13, font=("微软雅黑", 12))
search1.grid(row=4, column=0)  # 防止赋值为None

# 输出用例文本框
Label4 = Label(mainwindow, text='输出窗口', font=(
    "微软雅黑", 11)).grid(row=3, column=3, sticky=W + E)
search2 = scrolledtext.ScrolledText(mainwindow, width=50, height=13, font=("微软雅黑", 12))
search2.grid(row=4, column=3)  # 防止赋值为None

# 按钮集合
Button(mainwindow, text='查询正交表', width=10, command=lambda: do_func()) \
    .grid(row=3, column=0, sticky=W, padx=5, pady=3)
Button(mainwindow, text='编辑提示', width=10, command=lambda: show_detail()) \
    .grid(row=3, column=0, sticky=E, padx=5, pady=3)
Button(mainwindow, text='用例输出', width=10, command=lambda: get_data()) \
    .grid(row=3, column=1, sticky=E, padx=5, pady=3)
Button(mainwindow, text='关于工具', width=10, command=lambda: show_about()) \
    .grid(row=2, column=1, padx=5, pady=3)
Button(mainwindow, text='退出程序', width=10, command=lambda: quit_waining()) \
    .grid(row=4, column=1, sticky=E + S, padx=5, pady=3)
Button(mainwindow, text='首次使用帮助', width=10, command=lambda: show_help1()) \
    .grid(row=1, column=1, sticky=N, padx=5, pady=3)
Button(mainwindow, text='导出用例', width=10, command=lambda: export_to_file(result, name, int(index.get()))) \
    .grid(row=3, column=3, sticky=W, padx=5, pady=3)
Button(mainwindow, text='输出帮助', width=10, command=lambda: show_help2()) \
    .grid(row=3, column=3, sticky=E, padx=5, pady=3)
Button(mainwindow, text='打开当前\n文件夹', width=10, command=lambda: open_in_windows()) \
    .grid(row=2, column=3, sticky=E, padx=5, pady=3)
Button(mainwindow, text='正交表导出', width=10, command=lambda: export_list(result)) \
    .grid(row=2, column=3, sticky=W, padx=5, pady=3)


# ----------部分功能运行函数---------- #
def open_in_windows():  # 打开程序文件夹
    path_way = os.path.dirname(os.path.realpath(__file__))
    os.startfile(path_way)


def get_data():  # 输入具体值并载入列表
    if len(result):  # 是否已查找到数据
        read = search1.get('0.0', END).split("\n")
        if read == ['', '']:
            show_warning('你还没有在输入框输入数据呢（')
            return  # 结束运行
        input_diction.clear()
        name.clear()
        combine_text(read, input_diction, name)  # 读取文本并生成索引字典
        search_key(input_diction, result, int(index.get()))  # 搜索字典并将值存入到result中
        print_input_diction()
    else:
        show_warning('Ops!!!\n你还没有寻找正交表\n请先寻找需要的正交表（')
        return


def do_func():  # 多函数调用
    if len(result):  # 若重复查询，则将列表清空
        result.clear()
    check(level.get(), index.get(), result)  # 检查合法性并执行
    res_print()


def res_print():  # 输出寻找正交表
    search2.config(state=NORMAL)  # 框可编辑
    search2.delete(1.0, END)  # 清空内容
    count = 1
    for i in result:
        search2.insert(END, "测试用例 " + str(count) + " : ")
        search2.insert(END, i)
        search2.insert(END, "\n")
        count = count + 1
    search2.insert(END, "共生成" + str(count - 1) + "个测试用例\n")
    search2.config(state=DISABLED)  # 框不可编辑


def print_input_diction():
    search2.config(state=NORMAL)  # 框可编辑
    search2.delete(1.0, END)  # 清空内容
    search2.insert(END, "具体测试用例输出顺序：")
    search2.insert(END, "    ".join(str(l) for l in name) + "\n")
    cunt2 = 1
    for i in result:
        search2.insert(END, "测试用例 " + str(cunt2) + " : ")
        for j in range(0, int(index.get())):
            search2.insert(END, i[j])
            if j < int(index.get()) - 1:
                search2.insert(END, " ")
        search2.insert(END, "\n")
        cunt2 = cunt2 + 1
    search2.insert(END, "共生成" + str(cunt2 - 1) + "个测试用例\n")
    search2.config(state=DISABLED)  # 框不可编辑


mainwindow.mainloop()
