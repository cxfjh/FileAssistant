from tkinter import Frame, Scrollbar, Text, Tk, font # 导入所需模块


# 创建次窗口
def secondaryWindow():
    root = Tk() # 创建窗口
    root.title("使用教程") # 设置窗口标题
    root.geometry("1000x530") # 设置窗口大小
    root.resizable(False, False) # 设置窗口不可缩放
    root.wm_attributes("-topmost", 1) # 设置窗口置顶

    frame = Frame(root, padx=10, pady=10) # 创建Frame
    frame.pack(fill="both", expand=True) # 填充Frame
    scrollbar = Scrollbar(frame) # 创建Scrollbar
    scrollbar.pack(side="right", fill="y") # 放置Scrollbar
    
    customFont = font.Font(size=100) # 设置字体大小
    text = Text(frame, wrap="word", yscrollcommand=scrollbar.set, font=customFont) # 创建Text
    text.pack(fill="both", expand=True) # 填充Text
    scrollbar.config(command=text.yview) # 绑定Scrollbar与Text

    # 插入文本内容
    tutorialText = """
    要使用管理员权限运行本程序，请右键选择“以管理员身份运行”或在命令行中输入“管理员”运行。
    要在U盘插入前运行程序才能获取得到U盘里面的文件。。

    
    参数1—文件名关键字:关键字

        说明:可以多写几个关键词，要用|分隔开。比如像这样：答案|doc|txt|考试|学|资料
        


    参数2—选择存放路径:C:\Windows\FakeSystem

        说明:如果为空，默认存放路径就是C:\Windows\FakeSystem
             可以更改其他路径，点击左边《选择存放路径》按钮即可，或自己手动输入

             
             
    参数3—盘符(默认U盘):C:

        说明:可以选择多个盘符,要用|分隔开。比如:C:\|F:\ 或者指定默认文件夹:C:\Windows|D:\Edge
             如果不输入任何路径，默认的就是U盘所有盘符。
    
             
    
    项目地址:https://github.com/cxfjh/FileAssistant
    联系作者:2449579731@qq.com
    """

    text.insert("1.0", tutorialText) # 插入文本内容
    text.config(state="disabled") # 禁用文本框编辑
    root.mainloop() # 显示窗口

