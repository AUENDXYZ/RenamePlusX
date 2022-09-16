#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter.messagebox import Message
from tkinter.ttk import *
# from tkinter import *
from configparser import ConfigParser

# 判断是为 文件 或 目录 进行改名, On 则仅为目录改名(True), Off 则仅为文件改名(False)
set_file_dir = False
cfg_path = os.getcwd()

# --------------------------- 主窗体的设置 -------------------------------
win = tk.Tk()
win.title("文件-目录 批量改名小工具 RenamePlusX v0.2 --- AUEND@163.com ")
s_width = str(int((win.winfo_screenwidth()-800)/2))
s_height = str(int((win.winfo_screenheight()-600)/2))
position = f"800x600+{s_width}+{s_height}"    # 使窗口居中显示, x 是字母 x
win.geometry(position)
win.config(bg='white')
win.iconbitmap('./Resources/logo.ico')
win.minsize(800,600)
win.attributes('-topmost', True)              # 置顶窗口
win.attributes("-alpha", 0.9)                 # 设置窗口透明度，透明度的值是：0~1 可以是小数点，0：全透明；1：全不透明
win.resizable(True,False)                     # 窗体设置为False,则不可改变大小(X,Y)

# ---------------------------- 导入全部图片素材 -----------------------------
img_play = tk.PhotoImage(file='./img_play.png')
img_dir_on = tk.PhotoImage(file='./img_dir_on.png')
img_dir_off = tk.PhotoImage(file='./img_dir_off.png')
img_quit_on = tk.PhotoImage(file='./img_quit_on.png')

# ------------ 放置 text 控件,用来显示和增改需要去除的特殊字符串 -------------

text_del = scrolledtext.ScrolledText(win, font=('msyh',16,'bold'),
                bg='lightyellow',           # 控件的背景颜色
                fg='blue',                  # 字符的颜色
                width = 64, height=19,      # 控件的宽度和高度
                state=tk.NORMAL,               # 状态为正常可用
                undo= True,                 # 可以撤消操作
                exportselection=True,       # 选中时即会复制内容
                wrap=None )                 # 如果文字太长时的处理,其中 x 轴的滚动条要显示则必须 wrap=None
text_del.grid(  row=0, column=0,
                padx=8, pady=8,     # 控件离窗体的左右和上下边界距离
                columnspan=3)       # Grid 包含下面的3个label的 Grid


# ------------------------ 几个按钮的对应功能函数 ------------------------------

def set_file_dir():
    global set_file_dir
    if not set_file_dir:
        btn_dir.config(image=img_dir_on, text='On 仅目录')
        set_file_dir = True
    else:
        btn_dir.config(image=img_dir_off, text='Off 仅文件')
        set_file_dir = False


def readtxt():
    lst_config_value = []
    with open('setting.txt', 'r', encoding='utf-8') as f1:
        for line in f1.readlines():
            lst_config_value.append(line)

        for v in lst_config_value:
            text_del.insert(tk.END, str(v))
    return lst_config_value

def quit_set():
    t = text_del.get('0.0', 'end')
    text_del_strings = t.split('\n')
    text_del_strings = set(text_del_strings)
    text_del_strings = list(text_del_strings)
    while text_del_strings.count('')>0:
        text_del_strings.remove('')
    with open('setting.txt', 'w+', encoding='utf-8') as f2:
        for line in text_del_strings:
            f2.write(str(line)+'\n')
    win.quit()


def rename_file_dir():
    global set_file_dir
    global lst_ok
    lst_ok = []
    path = filedialog.askdirectory()
    print('\n当前操作的目录为: ', path, '\n')

    # 从右边开始的替换字符串自定义函数 rreplace()
    def rreplace(self, old, new, *max):
        count = len(self)
        if max and str(max[0]).isdigit():
            count = max[0]
        while count:
            index = self.rfind(old)
            if index >=0:
                chunk = self.rpartition(old)
                self = chunk[0] + new + chunk[2]
            count -= 1
        return self

    if set_file_dir==False:

        def find_file(path):
            lst_all_file = []
            for r,d,f in os.walk(path):
                for file in f:
                    if os.path.isfile(os.path.join(r,file)):
                        lst_all_file.append(os.path.join(r,file))
            return lst_all_file

        def find_delfile(lst_allfile):
            lst_delfile = []
            for f_path in lst_allfile:
                fname = f_path.split('\\')[-1]
                if fname.find(delstr)>=0:
                    del_name = f_path.split('\\')[0:len(f_path)]
                    del_file = '\\'.join(del_name)
                    lst_delfile.append(del_file)
            return lst_delfile

        def rename_files(lst_delfile):
            if len(lst_delfile)>0:
                for f in lst_delfile:
                    f_new = rreplace(str(f), delstr, '', 1)
                    lst_ok.append(f_new)
                    os.rename(f, f_new)
            else:
                print('暂时没有找到符合改名特点的文件或文件夹!')
            return lst_ok

        for d in lst_delstr:
            delstr = d
            lst_allfile = find_file(path)
            lst_delfile = find_delfile(lst_allfile)
            lst_ok = rename_files(lst_delfile)

        if len(lst_ok)>0:
            print('\n-------------- 已经完成了以下文件和文件夹的改名: --------------\n')
            print(lst_ok)

    if set_file_dir==True:
        print('=================== 现在只是对目录进行操作... =====================')

        def alldir():
            global lst_deldir
            global lst_deldir_new
            lst_alldir = []
            lst_deldir = []
            lst_deldir_new = []

            for r,d,f in os.walk(path):
                lst_alldir.append(r)

            lst_alldir = lst_alldir[1:]
            lst_alldir = lst_alldir[::-1]

            for d in lst_alldir:
                dir_path = (d[::-1].split( '\\', 1 ))[1][::-1]  # 文件夹的父路径
                dir_name = (d[::-1].split( '\\', 1 ))[0][::-1]  # 文件夹的名称
                if dir_name.find(delstr)>=0:
                    lst_deldir.append(os.path.join(dir_path, dir_name))
                    dir_name_new = dir_name.replace(delstr, '')
                    lst_deldir_new.append(os.path.join(dir_path, dir_name_new))

            return lst_deldir, lst_deldir_new

        def renamedir(lst_deldir, lst_deldir_new):
            if len(lst_deldir_new)>0:
                for i in range(len(lst_deldir_new)):
                    shutil.move( lst_deldir[i], lst_deldir_new[i] )
                print('\n----------- 已经完成了全部文件夹的更名操作 ----------\n')
                print('  原目录: ', lst_deldir)
                print('\n----------------修改后目录名为: ---------------\n', lst_deldir_new)
            else:
                print('------------ 没有找到符合条件的文件夹! -----------------')

        for delstr_dir in lst_delstr:
            delstr = delstr_dir
            lst_deldir_tup = alldir()
            print(lst_deldir_tup)
            renamedir(lst_deldir_tup[0], lst_deldir_tup[1])


btn_dir = tk.Button(win, text='Off 仅文件', command=set_file_dir, bg='white', image=img_dir_off, compound='top', relief='flat')
btn_dir.grid( row=1, column=0, sticky=tk.W, padx=20, pady=20, ipadx=20, ipady=20 )

btn_play = tk.Button(win, command=rename_file_dir, bg='white', image=img_play, cursor='star', relief='flat')
btn_play.grid( row=1, column=1 )

btn_quit = tk.Button(win, command=quit_set, bg='white', image=img_quit_on, relief='flat')
btn_quit.grid( row=1, column=2, sticky=tk.E, padx=20, pady=20, ipadx=20, ipady=20 )

# 启动时自动读取 setting.ini 中的原有特殊字符串
lst_delstr = readtxt()

win.mainloop()

