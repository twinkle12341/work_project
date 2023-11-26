# -*- coding: utf-8 -*-
""" 
@Time    : 2023/2/12 15:52
@Author  : Lee
@FileName: tank01.py
@SoftWare: PyCharm
"""
import random
import time

import pygame


class MainGame:
    """
    主逻辑类
    """
    pygame.font.init()
    font = pygame.font.SysFont("kaiti", 20)
    window = None
    myTank = None
    enemyTank = []
    enemyTankNum = 5
    # 游戏主界面
    WINDOW_HEIGHT = 500
    WINDOW_WIDTH = 1000
    # 存储我方坦克子弹
    myBullet = []
    myBulletNum = 3
    # 存储敌方子弹
    enemyBullet = []
    # 爆炸列表
    explodeList = []

    def startGame(self):
        """
        开始游戏
        :return:
        """
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([MainGame.WINDOW_WIDTH, MainGame.WINDOW_HEIGHT])
        # 设置标题
        pygame.display.set_caption("坦克大战v1")
        # 初始化用户坦克
        MainGame.myTank = Tank(475, 450)
        # 初始化敌方坦克
        self.creatEnemyTank()

        # 让窗口持续刷新
        while True:
            # 给窗口填充颜色
            self.window.fill([0, 100, 0])
            # 敌方剩余坦克文字显示
            enemyTankCout = "剩余地方坦克:" + str(MainGame.enemyTankNum) + "辆"
            MainGame.window.blit(MainGame.font.render(enemyTankCout, True, [0, 0, 0]), [10, 10])
            # 坦克显示
            MainGame.myTank.displayTank()
            # 持续移动坦克
            MainGame.myTank.move()
            # 显示敌方坦克
            self.blitEnemyTank()
            self.enemyTankMove()
            # 我方子弹显示和移动
            self.blitMyBullet()
            # 敌方子弹显示和移动
            self.blitEnemyBullet()
            self.displayExplodes()
            # 刷新界面
            pygame.display.update()
            # 获取按键和鼠标事件
            self.getEvent()
            time.sleep(0.02)

    def blitEnemyBullet(self):
        """
        显示敌方子弹
        :return:
        """
        for bullet in MainGame.enemyBullet:
            if bullet.stopShow:
                MainGame.enemyBullet.remove(bullet)
            else:
                bullet.displayBullet()
                bullet.move()

    def endGame(self):
        """
        结束游戏
        :return:
        """
        print("谢谢使用")
        # 结束python解释器
        exit()

    def creatEnemyTank(self):
        """
        初始化敌方坦克
        :return:
        """
        for i in range(MainGame.enemyTankNum):
            MainGame.enemyTank.append(EnemyTank(100, 3))

    def blitEnemyTank(self):
        """
        展示敌方坦克
        :return:
        """
        for tank in MainGame.enemyTank:
            if tank.live:
                tank.displayTank()
                index = random.randint(1, 1000)
                if index <= 20:
                    MainGame.enemyBullet.append(Bullet(tank.direction, tank.rect))
            else:
                MainGame.enemyTank.remove(tank)

    def blitMyBullet(self):
        """
        显示我方子弹
        :return:
        """
        for bullet in MainGame.myBullet:
            if bullet.stopShow:
                MainGame.myBullet.remove(bullet)

            else:
                #  我方子弹和敌方坦克碰撞
                bullet.hitEnemyTank()
                bullet.displayBullet()
                bullet.move()

    def enemyTankMove(self):
        """
        敌方坦克移动
        :return:
        """
        for tank in MainGame.enemyTank:
            tank.randMove()

    def getEvent(self):
        """
        获取鼠标和键盘的事件
        :return:
        """
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    MainGame.myTank.direction = 'L'
                    MainGame.myTank.stopFlag = False
                elif event.key == pygame.K_RIGHT:
                    MainGame.myTank.direction = 'R'
                    MainGame.myTank.stopFlag = False
                elif event.key == pygame.K_UP:
                    MainGame.myTank.direction = 'U'
                    MainGame.myTank.stopFlag = False
                elif event.key == pygame.K_DOWN:
                    MainGame.myTank.direction = 'D'
                    MainGame.myTank.stopFlag = False
                elif event.key == pygame.K_SPACE:
                    if len(MainGame.myBullet) < MainGame.myBulletNum:
                        MainGame.myBullet.append(Bullet(MainGame.myTank.direction, MainGame.myTank.rect))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    MainGame.myTank.stopFlag = True

    def displayExplodes(self):
        """
        展示爆炸效果
        :return:
        """
        for explode in MainGame.explodeList:
            if explode.live:
                explode.displayExplode()

class BaseItem(pygame.sprite.Sprite):
    def __int__(self):
        pygame.sprite.Sprite.__init__(self)


class Tank(BaseItem):
    """
    坦克基类
    """

    def __init__(self, hor, ver):
        MU = pygame.image.load('..\\image\\myUp.png').convert_alpha()
        MU = pygame.transform.smoothscale(MU, (50, 50))

        MD = pygame.image.load('..\\image\\myDown.png').convert_alpha()
        MD = pygame.transform.smoothscale(MD, (50, 50))

        ML = pygame.image.load('..\\image\\myLeft.png').convert_alpha()
        ML = pygame.transform.smoothscale(ML, (50, 50))

        MR = pygame.image.load('..\\image\\myRight.png').convert_alpha()
        MR = pygame.transform.smoothscale(MR, (50, 50))

        self.tanks = {
            'U': MU,
            'D': MD,
            'L': ML,
            'R': MR
        }
        self.direction = 'U'
        self.tank = self.tanks[self.direction]
        self.rect = self.tank.get_rect()
        self.rect.left = hor
        self.rect.top = ver
        self.speed = 3
        self.stopFlag = True

    def move(self):
        if not self.stopFlag:
            if self.direction == 'U' and self.rect.top > 0:
                self.rect.top -= self.speed
            elif self.direction == 'D' and self.rect.top + self.rect.height < MainGame.WINDOW_HEIGHT:
                self.rect.top += self.speed
            elif self.direction == 'L' and self.rect.left > 0:
                self.rect.left -= self.speed
            elif self.direction == 'R' and self.rect.left + self.rect.width < MainGame.WINDOW_WIDTH:
                self.rect.left += self.speed

    def shot(self):
        pass

    def displayTank(self):
        self.tank = self.tanks[self.direction]
        MainGame.window.blit(self.tank, self.rect)


class MyTank(Tank):
    """
    我方坦克
    """

    def __init__(self, ):
        pass


class EnemyTank(Tank):
    """
    敌方坦克
    """

    def __init__(self, top, speed):
        MU = pygame.image.load('..\\image\\enemyUp.png').convert_alpha()
        MU = pygame.transform.smoothscale(MU, (50, 50))

        MD = pygame.image.load('..\\image\\enemyDown.png').convert_alpha()
        MD = pygame.transform.smoothscale(MD, (50, 50))

        ML = pygame.image.load('..\\image\\enemyLeft.png').convert_alpha()
        ML = pygame.transform.smoothscale(ML, (50, 50))

        MR = pygame.image.load('..\\image\\enemyRight.png').convert_alpha()
        MR = pygame.transform.smoothscale(MR, (50, 50))

        self.tanks = {
            'U': MU,
            'D': MD,
            'L': ML,
            'R': MR
        }
        self.direction = self.randDirection()
        self.tank = self.tanks[self.direction]
        self.rect = self.tank.get_rect()
        self.rect.left = self.randPositon()
        self.rect.top = top
        self.speed = speed
        self.stopFlag = False
        self.step = 50
        self.live = True

    def randDirection(self):
        """
        随机生成敌方坦克的初始方向
        :return:
        """
        randDirection = random.randint(1, 4)
        if randDirection == 1:
            return 'U'
        elif randDirection == 2:
            return 'D'
        elif randDirection == 3:
            return 'L'
        else:
            return 'R'

    def randPositon(self):
        """
        随机生成敌方坦克的位置
        :return:
        """
        randPosition = random.randint(1, 9)
        return randPosition * 100

    def displayEnemyTank(self):
        """
        显示地方坦克
        :return:
        """
        super().displayTank()

    def randMove(self):
        """
            坦克随机移动
        :return:
        """
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 50
        else:
            super().move()
            self.step = self.step - 1


class Bullet(BaseItem):
    """direction
    子弹类，子弹位置、坐标、移动速度、移动
    """

    def __init__(self, direction, rect):
        self.bullet = pygame.image.load('..\\image\\enemyUp.png').convert_alpha()
        self.bullet = pygame.transform.smoothscale(self.bullet, (5, 5))
        self.direction = direction
        self.rect = self.bullet.get_rect()
        if direction == "U":
            self.rect.left = rect.left + rect.width / 2 - self.rect.width / 2
            self.rect.top = rect.top
        elif direction == "D":
            self.rect.left = rect.left + rect.width / 2 - self.rect.width / 2
            self.rect.top = rect.top + rect.height
        elif direction == "R":
            self.rect.left = rect.left + rect.width
            self.rect.top = rect.top + rect.height / 2 - self.rect.height / 2
        else:
            self.rect.left = rect.left
            self.rect.top = rect.top + rect.height / 2 - self.rect.height / 2
        self.speed = 5
        self.stopShow = False

    def move(self):
        """
        子弹移动
        :return:
        """
        if self.direction == "U":
            if self.rect.top + self.rect.height <= 0:
                self.stopShow = True
            else:
                self.rect.top -= self.speed
        elif self.direction == "D":
            if self.rect.top - self.rect.height >= MainGame.WINDOW_HEIGHT:
                self.stopShow = True
            else:
                self.rect.top += self.speed
        elif self.direction == "L":
            if self.rect.left + self.rect.width <= 0:
                self.stopShow = True
            else:
                self.rect.left -= self.speed
        else:
            if self.rect.left - self.rect.width >= MainGame.WINDOW_WIDTH:
                self.stopShow = True
            else:
                self.rect.left += self.speed

    def displayBullet(self):
        MainGame.window.blit(self.bullet, self.rect)

    def hitEnemyTank(self):
        """
        我方子弹碰到敌方坦克
        :return:
        """
        for eTank in MainGame.enemyTank:
            if pygame.sprite.collide_rect(eTank, self):
                self.stopShow = True
                eTank.live = False
                explode = Explode(eTank)
                MainGame.explodeList.append(explode)
                MainGame.enemyTankNum -= 1


class Explode:
    """
    爆炸类
    """

    def __init__(self, tank):
        self.rect = tank.rect
        self.step = 0
        MU1 = pygame.image.load('..\\image\\enemyUp.png').convert_alpha()
        MU1 = pygame.transform.smoothscale(MU1, (5, 5))
        MU2 = pygame.image.load('..\\image\\enemyUp.png').convert_alpha()
        MU2 = pygame.transform.smoothscale(MU2, (10, 10))
        MU3 = pygame.image.load('..\\image\\enemyUp.png').convert_alpha()
        MU3 = pygame.transform.smoothscale(MU3, (15, 15))
        MU4 = pygame.image.load('..\\image\\enemyUp.png').convert_alpha()
        MU4 = pygame.transform.smoothscale(MU4, (20, 20))
        MU5 = pygame.image.load('..\\image\\enemyUp.png').convert_alpha()
        MU5 = pygame.transform.smoothscale(MU5, (30, 30))
        self.images = [MU1, MU2, MU3, MU4, MU5]
        self.image = self.images[self.step]
        self.live = True

    def displayExplode(self):
        if self.step < len(self.images):
            MainGame.window.blit(self.images[self.step], self.rect)
            self.step += 1
        else:
            self.live = False
            self.step = 0


class Wall:
    """
    墙壁类
    """

    def __init__(self):
        pass

    def displayWall(self):
        pass


class Music:
    """
    音效类控制
    """

    def __init__(self):
        pass

    def play(self):
        pass


if __name__ == '__main__':
    window = MainGame()
    window.startGame()
