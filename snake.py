#snake.py
from turtle import *
from random import choice
from time import sleep
from pathfinding import GameGraph,pathfinding
global a, flag, tp, sp, b, s, gap, q, p, w0, f0
a, flag, tp, b, s,sp, gap, q, p, w0, f0=GameGraph()
class Block_constructio(Turtle):
    def __init__(self):  # 初始化方法，每个格子都是一只方形的turtle
        Turtle.__init__(self, shape='square')
        self.pu()  # 将画笔提起，不用画出轮廓，只保留填充部分，因为绘画的重心是方块而不是线
        self.color('white', 'white')  # 颜色格式为'边框','填充'

def frame():
    speed(0)
    listen()  # 开始接收键盘输入
    setup(400, 400)
    tracer(False)
    setworldcoordinates(-40, -40, 220, 220)
    for y in range(10):      # 为优化观感，在格子之间加上间隙,每个方块右边的空隙，共100个，每行最右放个占位的0
        for x in range(9):
            gap.append(Block_constructio())
            gap[-1].goto(x * 20 + 10, y * 20)
        gap.append(0)
    for y in range(9):  # 每个方块上边的空隙，共90个，最上行没有存放
        for x in range(10):
            gap.append(Block_constructio())
            gap[-1].goto(x * 20, y * 20 + 10)
    # 先放间隙再生成场地，因为后生成的会在上层
    for y in range(10):  # 生成场地
        for x in range(10):
            s.append(Block_constructio())
            s[-1].goto(x * 20, y * 20)
    s[45].color('blue', 'blue')  # 画出初始蛇
    s[44].color('purple', 'purple')

def move():
    if p:
        bcolor(0, 0)
        s[b.pop(0)].color('white', 'white')
        b.append(p.pop(0))
        s[b[-1]].color('purple', 'blue')
        s[b[-2]].fillcolor('purple')
        bcolor(-2, 1)
        update()
        sleep(sp)
    else:  # 到了食物跟前
        s[b[-1]].fillcolor('purple')
        b.append(a)
        s[a].color('purple', 'blue')
        bcolor(-2, 1)
        feed()
        update()
        sleep(sp)

def bcolor(n, c):  # 方块间隙颜色控制，n为身体索引号，c为颜色，1紫0白
    d = b[n + 1] - b[n]  # 判断方向，1向右，-1向左，10向上，-10向下
    if d == 1:  # 向右
        if c:  # 1，绿色
            gap[b[n]].color('purple', 'purple')
        else:  # 0，白色
            gap[b[n]].color('white', 'white')
    elif d == -1:
        if c:
            gap[b[n] - 1].color('purple', 'purple')
        else:
            gap[b[n] - 1].color('white', 'white')
    elif d == 10:
        if c:
            gap[b[n] + 100].color('purple', 'purple')
        else:
            gap[b[n] + 100].color('white', 'white')
    else:
        if c:
            gap[b[n] + 90].color('purple', 'purple')  # 加90是因为减10再加100
        else:
            gap[b[n] + 90].color('white', 'white')

def feed():
    global a
    choose = list(set(range(100)) - set(b))
    if choose:
        a = choice(choose)  # 作全场和蛇身的差集，再随机取点
        s[a].color('red', 'red')
    else:
        print('YOU WIN!')
        done()  # 吃满了，游戏结束

def going():
    while True:
        flag = 2
        p.clear()  # rBFS要预备p
        flag = pathfinding(b[-1], a, 'rBFS')  # 寻路，现在p里有路径了
        if flag == 1:
            flag = 2
            tp = b.copy()  # tBFS要预备tp
            tp.extend(p)  # 现在tp是蛇尾到食物的路径
            flag = pathfinding(a, tp[-(len(b))], 'tBFS')  # 检查：假如蛇按照rBFS寻到的路径吃了食物，蛇头与蛇尾间有无通路

        if flag == 1:  # 去吃食物是安全的，因为吃了食物后蛇头与蛇尾间仍有通路
            move()
        else:  # 蛇头和食物间无通路，只好“试探”一步
            p.clear()
            flag = pathfinding(b[-1], b[0], 'rBFS')  # 走那条通向蛇尾的路
            tail = b[0]
            bcolor(0, 0)
            if p:
                s[b.pop(0)].color('white', 'white')
                b.append(p.pop(0))
            else:  # 蛇头紧贴蛇尾时
                b.append(b.pop(0))
            s[b[-1]].color('purple', 'blue')
            s[b[-2]].fillcolor('purple')
            bcolor(-2, 1)
            update()
            sleep(sp)

