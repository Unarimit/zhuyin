import Processor
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import re

# job = Processor.Processor(mode=Processor.PlayMode.TO_ROMAJI)
# job = Processor.Processor()
# job.process()
mode = Processor.PlayMode.HIRA_ZHUYIN
is_cache = False  # 是否对cache进行替换，用于多文件


def openfile() -> None:
    filePath = str(filedialog.askopenfilename(filetypes=[("No Extend", "*.*")]))
    if filePath is None or filePath == '':
        return

    if len(filePath.split('.')) != 1:
        tk.messagebox.askquestion(title='提示', message='这个格式不行！')
        return

    filename = filePath.split('/')[-1]
    operate_bat = False
    if re.fullmatch(r'.*\d', filename) is None:
        print(filename)
        if re.fullmatch(r'.*\dbak', filename) is not None:
            filePath = filePath[:-3]
            operate_bat = True
        else:
            tk.messagebox.askquestion(title='提示', message='文件名称应该全是数字！，或者是*bak')
            return

    print(filePath)
    # do transform
    job = Processor.Processor(v.get())
    if operate_bat is False:
        result = job.process(filePath)
    else:
        result = job.process(filePath+'bak')

    if result == '':
        tk.messagebox.askquestion(title='提示', message='Unicode 解码失败, 请确认是否为歌词文件')

    if operate_bat is False and os.path.isfile(filePath+'bak'):
        tk.messagebox.askquestion(title='提示', message='已存在bak，请对bak操作')
        return

    if operate_bat is False:
        os.rename(filePath, filePath+"bak")

    f = open(filePath, encoding='utf-8', mode='w+')
    f.write(result)

    tk.messagebox.askquestion(title='提示', message='完成替换！')


def openfolder() -> None:
    folderName = tk.filedialog.askdirectory()
    if folderName is None or folderName == '':
        return
    count = 0
    for dirpath, dirnames, filenames in os.walk(folderName):
        for filename in filenames:
            filePath = dirpath + '/' + filename
            print(filePath)
            if process_single_file(filePath) is True:
                count += 1
    tk.messagebox.askquestion(title='提示', message='完成替换！共' + str(count) + '个文件')


def open_cache_folder() -> None:
    global is_cache
    is_cache = True
    openfolder()
    is_cache = False


def process_single_file(filePath: str) -> bool:
    if filePath is None or filePath == '':
        return False

    if len(filePath.split('.')) != 1:
        return False

    filename = filePath.split('/')[-1]
    operate_bat = False  # 不对bak操作
    if is_cache is False:
        if re.fullmatch(r'.*\d', filename) is None:
            return False
    else:
        if re.search('bak', filename) is not None:
            return False

    # do transform
    job = Processor.Processor(v.get())
    if operate_bat is False:
        result = job.process(filePath)
    else:
        result = job.process(filePath+'bak')

    if result == '':
        return False

    if operate_bat is False and os.path.isfile(filePath+'bak'):
        return False

    if operate_bat is False:
        os.rename(filePath, filePath+"bak")

    f = open(filePath, encoding='utf-8', mode='w+')
    f.write(result)

    return True


def openfolder_restore_bak() -> None:
    folderName = tk.filedialog.askdirectory()
    if folderName is None or folderName == '':
        return
    count = 0
    for dirpath, dirnames, filenames in os.walk(folderName):
        for filename in filenames:
            if re.search('bak', filename) is not None:
                continue
            filePath = dirpath + '/' + filename
            if os.path.isfile(filePath + 'bak'):
                print(filePath)
                os.remove(filePath)
                os.rename(filePath + 'bak', filePath)
                count += 1

    tk.messagebox.askquestion(title='提示', message='还原了' + str(count) + '个文件')


def mode_change() -> None:
    global mode
    mode = v


root = tk.Tk()
v = tk.IntVar()
tk.Label(root, text='替换完之后，会把原来的文件名加上bak后，保存在原来的目录下，也可以对[数字+bak]的备份文件进行转换').pack()
tk.Radiobutton(root, text='平假名注音', command=mode_change, variable=v, value=1).pack()
tk.Radiobutton(root, text='平假名注音,大括号阔起汉字部分', command=mode_change, variable=v, value=4).pack()
tk.Radiobutton(root, text='片假名注音', command=mode_change, variable=v, value=2).pack()
tk.Radiobutton(root, text='变成罗马音', command=mode_change, variable=v, value=3).pack()
tk.Button(root, text='替换文件', command=openfile).pack()
tk.Button(root, text='替换文件夹下所有文件, [有bak的](已经替换过的)不会替换', command=openfolder).pack()
tk.Button(root, text='替换**缓存**文件夹下所有文件, [有bak的](已经替换过的)不会替换', command=open_cache_folder).pack()
tk.Button(root, text='通过bak还原指定文件夹中的所有歌词文件', command=openfolder_restore_bak).pack()
v.set(1)
root.mainloop()
