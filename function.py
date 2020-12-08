import tkinter.messagebox
import sys
import os


# ----------查询函数---------- #
def find(level, index, result):
    # 需要的变量
    detail = []  # 每次测试的内容
    state = 0  # 状态表示

    data = open("source.txt", "r", encoding='UTF-8')
    key = level + '^' + index  # 关键字段
    count = 0
    for line in data.readlines():
        if state == 1 and line != '\n':
            detail.append(line.split("\n")[0])  # 将数据读出
            temp = ",".join(detail[count])  # 为连续的数字分割
            result.append(temp.split(","[0]))  # 提取分割数字以list分别嵌入到result
            print(result)  # debug used
            count = count + 1
        if state == 1 and line == '\n':  # 当前正交表寻找完成
            break
        if state == 0:
            while key in line:
                show_warning('找到了:)即将输出用例')
                state = 1
                break
    for i in range(0, len(result)):
        print('测试用例', (i + 1), "选择项"': ', result[i])
    if state == 0:
        show_warning('貌似没有这个表呢')
    data.close()


# ----------输出实际用例函数部分---------- #
def combine_text(read_text, input_diction, name):  # 文本粘合并导入到字典
    """
    :param name: list
    :param read_text: list
    :type input_diction: list
    """
    letter_cache = []  # 单字缓存
    word_cache = []  # 当前行所有词语缓存
    w = []
    input_diction.clear()  # 清空上一次寻找的数据
    for cur_row in read_text:  # 按行拆词
        temp = "".join(cur_row)
        for letter in temp:  # 单行拆词识别
            if letter == "：" or letter == "，" or letter == "。" \
                    or letter == ":" or letter == "," or letter == ".":  # 中英文输入支持
                temp2 = "".join(letter_cache)
                word_cache.append(temp2)  # 满足要求时词语组合
                letter_cache.clear()  # 清除缓存
            else:
                letter_cache.append(letter)  # 单个词语入列表
        if len(word_cache) != 0:
            name.append(word_cache[0])  # 存取因素名
        for i in range(1, len(word_cache)):  # 当前因素水平的字典创建
            if len(word_cache) != 0:
                w.append(word_cache[i])
                # input_diction.setdefault(word_cache[0], {})[i - 1] = word_cache[i]  # 字典嵌入（有问题）
        print(w)
        if len(word_cache) != 0:
            input_diction.append(w.copy())
        print(input_diction)  # debug
        word_cache.clear()  # 清空当前行的所有词语，等待下一行存入
        w.clear()


def search_key(input_diction, result, row):  # 列表搜索
    for cur in result:
        state = 0
        for cur_list in input_diction:
            print(cur_list)  # debug
            cur[state] = cur_list[int(cur[state])]
            state = state + 1
        print(result)  # debug


# ---------导出测试用例--------- #
def export_to_file(result, name, index):
    if len(name) == 0:
        show_warning('你还没有执行用例输出呢（\n请先执行用例输出')
        return
    file = open("export.txt", 'w', encoding='UTF-8').close()  # 若文件先前存在，则清空文件内容
    f = open('export.txt', "w", encoding='UTF-8')
    print("以下是测试用例，子项目顺序为输入的因素的顺序\ne.g：",
          "    ".join(str(l) for l in name), "\n",
          "----------", file=f)
    count = 0
    for i in result:
        for j in range(0, index):
            f.write(i[j])
            if j < index - 1:
                f.write(" ")
        f.write('\n')
        count = count + 1
    print("----------"
          "\n共生成", count, "个测试用例", file=f)
    print(os.path.realpath("export.txt"))
    show_ok(str(os.path.realpath("export.txt")))


def export_list(result):
    if len(result) == 0:  # 是否已查找到数据
        show_warning('Ops!!!\n你还没有寻找正交表\n请先寻找需要的正交表（')
        return
    file = open("export.txt", 'w', encoding='UTF-8').close()  # 若文件先前存在，则清空文件内容
    f = open('export.txt', "w", encoding='UTF-8')
    print("查询的正交表输出",
          "\n----------", file=f)
    count = 0
    for i in result:
        for j in i:
            f.write(j)
            f.write(" ")
        f.write("\n")
        count = count + 1
    print("----------"
          "\n共生成", count, "个测试用例", file=f)
    print(os.path.realpath("export.txt"))
    show_ok(str(os.path.realpath("export.txt")))


# ----------UI界面相关函数---------- #
def show_warning(msg):
    tkinter.messagebox.showwarning("提示", msg)


def show_help1():
    tkinter.messagebox.showinfo(
        "使用帮助",
        "（本工具暂不支持混合正交表和非标准正交表）\n"
        "1. 先输入你想找的正交表水平与因素\n"
        "2. 查询成功后输入具体用例数据，\n"
        "3. 执行用例生成\n"
        "请先运行查表才能进行用例输出\n"
        "导出用例文件名为export.txt")


def show_detail():
    tkinter.messagebox.showinfo(
        "编辑提示",
        "输入样例\n"
        "因素1：水平1，水平2，水平3。\n"
        "因素2：水平1，水平2，水平3。\n"
        "每行请以句号或小数点结尾\n编辑器支持中英文符号混合输入\n"
        "如果需要重新输入测试用例，请先运行一次查表操作")


def show_about():
    tkinter.messagebox.showinfo(
        "关于工具",
        "版本：1.0.0\n"
        "由Lonely_Fantasy编写\n"
        "目前功能：简单标准正交表查询与用例生成"
    )


def show_ok(path):
    tkinter.messagebox.showinfo(
        "导出提示",
        "导出文件成功\n"
        "当前文件在" + path
    )


def show_help2():
    tkinter.messagebox.showinfo(
        "输出帮助",
        "本输出框输出用例测试和查表结果\n"
        "已设置输出框无法手动编辑"
    )


def quit_waining():
    value = tkinter.messagebox.askyesno('退出程序', '确认退出？')
    if value:
        sys.exit(0)
    else:
        return


# 有效性查验函数
def is_num(a, b):
    if a.isdigit() and b.isdigit():
        return True
    else:
        return False


def check(row, column, result):
    if is_num(row, column):
        find(row, column, result)
    else:
        show_warning('输入数据有误，请输入纯数字（')
