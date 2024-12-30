import wmi # 用于监控U盘插入
import os # 用于文件操作
import shutil # 用于文件复制
import pythoncom # 用于初始化COM组件
from tkinter import filedialog # 用于文件对话框
from concurrent.futures import ThreadPoolExecutor # 用于并发处理文件复制


# 选择文件夹路径并返回路径
def selectFilePath():
    try: return filedialog.askdirectory()
    except: pass


# 检测U盘插入
def detectUsb():
    try:
        pythoncom.CoInitialize() # 初始化COM组件
        wmiObj = wmi.WMI() # 初始化WMI对象
        notification_filter = wmiObj.Win32_DeviceChangeEvent # 定义通知过滤器
        wmiEvent = wmiObj.watch_for(notification_type=notification_filter, raw_wql="SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_PnPEntity'") # 定义WMI事件
        while True: # 循环监控
            usbInserted = wmiEvent()  # 等待WMI事件
            if usbInserted is None: continue  # 忽略空事件
            return [usb.DeviceID for usb in wmiObj.Win32_LogicalDisk() if usb.DriveType == 2] # 返回插入的U盘列表
    except: pass


# 生成唯一的文件名
def ensureUniqueFilename(destinationFolder, filename):
    baseName, ext = os.path.splitext(filename) # 分离文件名和扩展名
    counter = 1 # 定义计数器
    while True: # 循环生成唯一文件名 
        newFilename = f"{baseName}_{counter}{ext}" # 生成新文件名
        if not os.path.exists(os.path.join(destinationFolder, newFilename)): return newFilename # 如果文件名不存在，返回新文件名
        counter += 1 # 否则计数器加1


# 匹配多个关键字查找文件复制到指定文件夹
def multiFileCopy(sourceDrives, keywords, destinationFolder):
    try:
        if not os.path.exists(destinationFolder): os.makedirs(destinationFolder) # 检查目标文件夹是否存在，如果不存在则创建

        # 循环遍历每个sourceDrive盘符根据关键词查找文件并复制到目标文件夹
        for sourceDrive in sourceDrives:
            filesToCopy = [] # 定义待复制文件列表
            for root, dirs, files in os.walk(sourceDrive): # 递归遍历源驱动器中的所有文件和文件夹
                for file in files:
                    fileLower = file.lower() # 将文件名转换为小写形式
                    if any(keyword in fileLower for keyword in keywords): # 判断文件名中是否包含关键词
                        sourceFilePath = os.path.join(root, file) # 构建源文件路径
                        destinationFilePath = os.path.join(destinationFolder, file) # 构建目标文件路径

                        if os.path.exists(destinationFilePath): # 如果目标文件已存在，生成唯一文件名
                            newFilename = ensureUniqueFilename(destinationFolder, file) # 生成唯一文件名
                            destinationFilePath = os.path.join(destinationFolder, newFilename) # 更新目标文件路径

                        filesToCopy.append((sourceFilePath, destinationFilePath)) # 添加待复制文件到列表

            # 使用线程池并发地复制文件
            with ThreadPoolExecutor() as executor:
                for sourceFile, destinationFile in filesToCopy:
                    try: shutil.copy(sourceFile, destinationFile) # 尝试复制文件到目标文件夹
                    except Exception as e: pass # 如果出现异常，继续下一个文件的复制
    except: pass # 捕获异常，继续下一个盘符的处理

