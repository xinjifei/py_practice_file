import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random

# 定义方块顶点（立方体）
vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)

# 定义方块面
faces = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

# 定义方块面的颜色（不同面不同颜色）
colors = (
    (1, 0, 0), (1, 1, 0), (0, 1, 0),
    (0, 1, 1), (0, 0, 1), (1, 0, 1)
)

# 定义方块边
edges = (
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
)


# 生成随机地形
def generate_terrain(size=20, height=5):
    terrain = {}
    for x in range(-size, size):
        for z in range(-size, size):
            # 随机生成地面高度，模拟地形起伏
            y = random.randint(0, height)
            terrain[(x, y, z)] = True
            # 填充下方方块，形成实心地面
            for i in range(y):
                terrain[(x, i, z)] = True
    return terrain


# 绘制单个方块
def draw_cube():
    glBegin(GL_QUADS)
    for face in range(6):
        glColor3fv(colors[face])
        for vertex in faces[face]:
            glVertex3fv(vertices[vertex])
    glEnd()

    # 可选：绘制方块边框（便于调试）
    # glBegin(GL_LINES)
    # glColor3fv((0, 0, 0))
    # for edge in edges:
    #     for vertex in edge:
    #         glVertex3fv(vertices[vertex])
    # glEnd()


# 绘制整个世界
def draw_world(terrain):
    for position in terrain:
        x, y, z = position
        glPushMatrix()
        glTranslatef(x, y, z)
        draw_cube()
        glPopMatrix()


# 主游戏类
class MinecraftClone:
    # 加载纹理的方法（缩进4个空格，属于类内方法）
    def load_textures(self):
        # 函数体必须缩进（再4个空格，共8个）
        glEnable(GL_TEXTURE_2D)
        try:
            # 替换成你的图片路径（二选一）
            # 写法1（推荐）
            grass_texture = pygame.image.load("D:/py/python/python.exe D:/PythonProject/.idea/练习/bookshelf.png")
            # 写法2（备选）
            # grass_texture = pygame.image.load("D:\\py\\python\\python.exe D:\\PythonProject\\.idea\\练习\\bookshelf.png")

            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                         grass_texture.get_width(), grass_texture.get_height(),
                         0, GL_RGB, GL_UNSIGNED_BYTE,
                         pygame.image.tostring(grass_texture, "RGB"))
        except:
            self.texture_id = None
            print("纹理图片加载失败，使用纯色方块")

    # __init__方法（和load_textures同级，缩进4个空格）
    def __init__(self):
        pygame.init()
        display = (800, 600)
        # 先创建OpenGL上下文（关键！）
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        # 再开启深度测试
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        # 最后加载纹理（此时OpenGL上下文已就绪）
        self.load_textures()
        pygame.display.set_caption("简易我的世界")

        # 设置透视投影
        gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)

        # 玩家初始位置和视角
        self.player_x, self.player_y, self.player_z = 0, 5, 5
        self.yaw = 0  # 左右旋转
        self.pitch = 0  # 上下旋转

        # 鼠标锁定（第一人称视角）
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        # 生成地形
        self.terrain = generate_terrain()

        # 移动速度（优化手感）
        self.move_speed = 0.3
        self.mouse_sensitivity = 0.2

    def handle_input(self):
        # 获取键盘输入
        keys = pygame.key.get_pressed()

        # 计算移动方向（基于当前视角）
        rad_yaw = np.radians(self.yaw)
        forward_x = -np.sin(rad_yaw) * self.move_speed
        forward_z = -np.cos(rad_yaw) * self.move_speed

        # 前后移动（W/S）
        if keys[K_w]:
            self.player_x += forward_x
            self.player_z += forward_z
        if keys[K_s]:
            self.player_x -= forward_x
            self.player_z -= forward_z

        # 左右移动（A/D）
        if keys[K_a]:
            self.player_x += np.cos(rad_yaw) * self.move_speed
            self.player_z -= np.sin(rad_yaw) * self.move_speed
        if keys[K_d]:
            self.player_x -= np.cos(rad_yaw) * self.move_speed
            self.player_z += np.sin(rad_yaw) * self.move_speed

        # 上下移动（空格/左Shift）
        if keys[K_SPACE]:
            self.player_y += self.move_speed
        if keys[K_LSHIFT]:
            self.player_y -= self.move_speed

        # 退出游戏（ESC）
        if keys[K_ESCAPE]:
            pygame.quit()
            quit()

        # 鼠标控制视角
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        self.yaw += mouse_dx * self.mouse_sensitivity
        self.pitch -= mouse_dy * self.mouse_sensitivity

        # 限制俯仰角度（避免视角翻转）
        self.pitch = max(-89, min(89, self.pitch))

        # 方块操作（鼠标左键破坏，右键放置）
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                # 射线检测（简化版，获取玩家视线方向的方块）
                ray_x = int(round(self.player_x - np.sin(np.radians(self.yaw))))
                ray_y = int(round(self.player_y + np.sin(np.radians(self.pitch))))
                ray_z = int(round(self.player_z - np.cos(np.radians(self.yaw))))

                if event.button == 1:  # 左键破坏
                    if (ray_x, ray_y, ray_z) in self.terrain:
                        del self.terrain[(ray_x, ray_y, ray_z)]
                if event.button == 3:  # 右键放置
                    self.terrain[(ray_x, ray_y, ray_z)] = True


    def update_camera(self):
        # 重置视角
        glLoadIdentity()

        # 应用视角旋转
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)

        # 设置相机位置（OpenGL相机是反向的，所以用减号）
        glTranslatef(-self.player_x, -self.player_y, -self.player_z)

    def run(self):
        while True:
            # 处理输入
            self.handle_input()

            # 更新相机
            self.update_camera()

            # 清空屏幕
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # 绘制世界
            draw_world(self.terrain)

            # 更新显示
            pygame.display.flip()
            pygame.time.wait(10)


if __name__ == "__main__":
    game = MinecraftClone()
    game.run()