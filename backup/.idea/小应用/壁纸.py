import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu, QAction, QFileDialog
)
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import (
    Qt, QTimer, QSize, QThread, pyqtSignal, QRect
)


# 壁纸窗口类 - 每个显示器对应一个窗口
class WallpaperWindow(QWidget):
    def __init__(self, screen, parent=None):
        super().__init__(parent)
        self.screen = screen  # 绑定对应的显示器
        self.current_wallpaper = None

        # 设置窗口属性：无边框、置顶、背景透明、全屏
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnBottomHint |  # 置于最底层（壁纸层级）
            Qt.Tool  # 不显示在任务栏
        )
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明

        # 适配显示器尺寸和位置
        self.setGeometry(screen.geometry())

        # 用于显示壁纸的标签
        self.wallpaper_label = QLabel(self)
        self.wallpaper_label.setGeometry(self.rect())
        self.wallpaper_label.setScaledContents(True)  # 图片自适应标签大小

    # 设置壁纸图片
    def set_wallpaper(self, image_path):
        if not os.path.exists(image_path):
            print(f"壁纸文件不存在：{image_path}")
            return

        self.current_wallpaper = image_path
        pixmap = QPixmap(image_path)
        # 按显示器比例缩放图片（保持宽高比）
        scaled_pixmap = pixmap.scaled(
            self.screen.size(),
            Qt.KeepAspectRatioByExpanding,  # 铺满屏幕（超出部分裁剪）
            Qt.SmoothTransformation  # 平滑缩放
        )
        self.wallpaper_label.setPixmap(scaled_pixmap)


# 多屏壁纸引擎主类
class MultiScreenWallpaperEngine:
    def __init__(self, app):
        self.app = app
        self.app.setQuitOnLastWindowClosed(False)  # 关闭窗口不退出程序
        self.wallpaper_windows = []  # 存储每个显示器的壁纸窗口
        self.wallpaper_list = []  # 壁纸文件列表
        self.current_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.switch_wallpaper)  # 定时切换壁纸

        # 初始化系统托盘（方便操作）
        self.init_tray_icon()
        # 初始化所有显示器的壁纸窗口
        self.init_wallpaper_windows()

    # 初始化系统托盘图标和菜单
    def init_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self.app)
        self.tray_icon.setIcon(QIcon.fromTheme("wallpaper"))  # 系统默认图标

        # 托盘菜单
        tray_menu = QMenu()

        # 选择壁纸文件夹
        select_folder_action = QAction("选择壁纸文件夹", self.app)
        select_folder_action.triggered.connect(self.select_wallpaper_folder)
        tray_menu.addAction(select_folder_action)

        # 切换下一张壁纸
        next_wallpaper_action = QAction("下一张壁纸", self.app)
        next_wallpaper_action.triggered.connect(self.switch_wallpaper)
        tray_menu.addAction(next_wallpaper_action)

        # 自动切换（开启/关闭）
        self.auto_switch_action = QAction("开启自动切换", self.app)
        self.auto_switch_action.setCheckable(True)
        self.auto_switch_action.triggered.connect(self.toggle_auto_switch)
        tray_menu.addAction(self.auto_switch_action)

        # 退出程序
        exit_action = QAction("退出", self.app)
        exit_action.triggered.connect(self.app.quit)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    # 初始化所有显示器的壁纸窗口
    def init_wallpaper_windows(self):
        screens = self.app.screens()
        for screen in screens:
            window = WallpaperWindow(screen)
            self.wallpaper_windows.append(window)
            window.show()  # 显示壁纸窗口

    # 选择壁纸文件夹
    def select_wallpaper_folder(self):
        folder_path = QFileDialog.getExistingDirectory(None, "选择壁纸文件夹")
        if not folder_path:
            return

        # 筛选支持的图片格式
        supported_formats = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
        self.wallpaper_list = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if os.path.splitext(f)[1].lower() in supported_formats
        ]

        if self.wallpaper_list:
            # 为所有显示器设置第一张壁纸
            self.current_index = 0
            self.apply_wallpaper(self.wallpaper_list[self.current_index])
        else:
            print("所选文件夹中没有支持的图片格式")

    # 为所有显示器应用指定壁纸
    def apply_wallpaper(self, wallpaper_path):
        for window in self.wallpaper_windows:
            window.set_wallpaper(wallpaper_path)

    # 切换下一张壁纸
    def switch_wallpaper(self):
        if not self.wallpaper_list:
            return

        self.current_index = (self.current_index + 1) % len(self.wallpaper_list)
        self.apply_wallpaper(self.wallpaper_list[self.current_index])

    # 开启/关闭自动切换
    def toggle_auto_switch(self, checked):
        if checked:
            self.timer.start(10000)  # 10秒切换一次（可自行修改）
            self.auto_switch_action.setText("关闭自动切换")
        else:
            self.timer.stop()
            self.auto_switch_action.setText("开启自动切换")


# 主程序入口
if __name__ == "__main__":
    # 安装依赖（如果未安装）：pip install PyQt5
    try:
        app = QApplication(sys.argv)
        engine = MultiScreenWallpaperEngine(app)
        sys.exit(app.exec_())
    except ImportError:
        print("请先安装PyQt5：执行命令 pip install PyQt5")
        sys.exit(1)