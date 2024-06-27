from random import choice
from time import sleep
from turtle import*
import auto_pathfinding
print("请选择实验模式，输入1即为贪吃蛇智能寻路，输入2即为蛇贪吃")
print("请输入你的选择:")
switch = eval(input())
if switch==1:
    auto_pathfinding.main_2()
if switch==2:
    print("*******请选择刷新速度******")
    print("******输入1即为每1s刷新一帧******")
    print("******输入2即为每0.3s刷新一帧******")
    print("******输入3即为每0.2s刷新一帧******")
    print("******输入4即为每0.1s刷新一帧******")
    print("******输入5即为默认刷新速度******")
    print("请选择你的速度:", end="")
    a = input()
    op = int(a)
    b1 = [0, 1, 2, 3]  # 绿色蛇蛇身，0为尾3为头
    b2 = [99, 98, 97, 96]  # 紫色蛇蛇身
    green = True  # 绿色蛇是否活着（没有绕进死路）
    purple = True

    flag = False  # False为未找到通向食物的路径，True为已找到
    score = 0  # 得分，蛇每走一步加一分
    cn = 4  # 食物走几帧蛇走一步，从4逐渐减少，直至玩家跟不上[手动滑稽]
    count = 0  # 食物走了凡帧

    a = 44  # 食物位置
    s = []  # 放格子实例
    wal = set()  # 放墙
    p1 = [100]  # 放寻得的一步路径，因为不能为空所以随便放个100
    p2 = [100]


    class Block(Turtle):
        def __init__(self):
            Turtle.__init__(self, shape='square')
            self.pu()
            self.color('white', 'silver')


    def wall():
        for i in range(3):
            ch = set(range(100)) - {44}  # 除去食物
            ch = ch - set(b1)  # 除去绿蛇
            ch = ch - set(b2)  # 除去紫蛇
            ch = ch - wal  # 除去已设置的障碍
            ww = choice(list(ch))
            wal.add(ww)
        for i in wal:
            s[i].fillcolor('black')


    def pressKeys():
        onkeypress(right, 'Right')
        onkeypress(down, 'Down')
        onkeypress(left, 'Left')
        onkeypress(up, 'Up')


    def disable():  # 防误触
        onkeypress(None, 'Right')
        onkeypress(None, 'Down')
        onkeypress(None, 'Left')
        onkeypress(None, 'Up')


    def right():
        global a
        disable()
        if a % 10 != 9 and a + 1 not in b1 + b2 and a + 1 not in wal:
            s[a].fillcolor('silver')
            a += 1
            s[a].fillcolor('red')


    def down():
        global a
        disable()
        if a > 9 and a - 10 not in b1 + b2 and a - 10 not in wal:
            s[a].fillcolor('silver')
            a -= 10
            s[a].fillcolor('red')


    def left():
        global a
        disable()
        if a % 10 != 0 and a - 1 not in b1 + b2 and a - 1 not in wal:
            s[a].fillcolor('silver')
            a -= 1
            s[a].fillcolor('red')


    def up():
        global a
        disable()
        if a < 90 and a + 10 not in b1 + b2 and a + 10 not in wal:
            s[a].fillcolor('silver')
            a += 10
            s[a].fillcolor('red')


    def detect(n, w, q):  # 判断v号方块周围方块的状态
        global flag
        if w[n] == 1:
            flag = True
            return 1
        elif w[n] == 2:
            w[n] = 0
            q.append(n)
            return 2


    def BFS(start, end, p):  # 蛇的寻路算法，参数为起点索引、终点索引、存储路径的表
        w = [2] * 100  # 列表w存放100个格子的状态，2为未搜索，1为终点，0为已搜索
        for i in b1 + b2:  # 把蛇身标记为已搜索
            w[i] = 0
        for i in wal:  # 把障碍标记为已搜索
            w[i] = 0
        w[end] = 1  # 标记终点
        q = [start]  # 队列初始化，加入起点
        f = [-1] * 100  # 列表f用于存放路径，记录每个格子“来自哪里”，-1为未存放
        while q:
            v = q[0]
            if 0 <= v + 1 <= 99 and v % 10 != 9:  # 右边
                r = detect(v + 1, w, q)
                if r == 1:
                    break
                elif r == 2:
                    f[v + 1] = v
            if 0 <= v + 10 <= 99:  # 上方
                r = detect(v + 10, w, q)
                if r == 1:
                    break
                elif r == 2:
                    f[v + 10] = v
            if 0 <= v - 1 <= 99 and v % 10 != 0:  # 左边
                r = detect(v - 1, w, q)
                if r == 1:
                    break
                elif r == 2:
                    f[v - 1] = v
            if 0 <= v - 10 <= 99:  # 下方
                r = detect(v - 10, w, q)
                if r == 1:
                    break
                elif r == 2:
                    f[v - 10] = v
            q.pop(0)
        while v != start:
            p[0] = v
            v = f[v]


    def greenmove(to):  # 绿蛇移动一格
        if op==1:
            sleep(1)  # 延迟0.1秒，减慢蛇的速度
        elif op==2:
            sleep(0.3)
        elif op==3:
            sleep(0.2)
        elif op==4:
            sleep(0.1)
        elif op==5:
            sleep(0)
        s[b1[0]].color('white', 'silver')
        s[b1[-1]].fillcolor('green')
        s[to].color('green', 'blue')
        b1.pop(0)
        b1.append(to)


    def purplemove(to):  # 紫蛇移动一格
        if op==1:
            sleep(0.4)  # 延迟0.1秒，减慢蛇的速度
        elif op==2:
            sleep(0.3)
        elif op==3:
            sleep(0.2)
        elif op==4:
            sleep(0.1)
        elif op==5:
            sleep(0)
        s[b2[0]].color('white', 'silver')
        s[b2[-1]].fillcolor('purple')
        s[to].color('purple', 'blue')
        b2.pop(0)
        b2.append(to)


    setup(400, 300)
    tracer(False)  # 忽略绘制过程
    setworldcoordinates(-100, -50, 283, 230)
    for y in range(10):  # 生成10*10场地，用s来装这些格子，最左下索引为0，右上为99
        for x in range(10):
            s.append(Block())
            s[-1].goto(x * 20, y * 20)

    for i in b1[:3]:  # 绘制绿蛇，其中蛇头为蓝色
        s[i].color('green', 'green')
    s[3].color('green', 'blue')

    for i in b2[:3]:
        s[i].color('purple', 'purple')
    s[96].color('purple', 'blue')

    s[44].fillcolor('red')  # 绘制食物

    wall()  # 生成障碍物

    ht()  # 计分功能
    pu()
    goto(-50, 80)
    write(score, font=('Arial', 20))

    update()
    pressKeys()
    listen()

    while 1:
        if count is cn:
            count = 0
            if green:
                flag = False
                BFS(b1[-1], a, p1)
                if p1[0] in b1:  # 如果寻得的路径在蛇身中，不是吃到了就是绕死了
                    s[b1[-1]].fillcolor('green')
                    if flag:
                        break
                    else:
                        green = False
                        print('绿蛇绕死了！')
                        continue
                greenmove(p1[0])
            # 绿蛇走过了，下面是紫蛇走
            if purple:
                flag = False
                BFS(b2[-1], a, p2)
                if p2[0] in b2:
                    s[b2[-1]].fillcolor('purple')
                    if flag:
                        break
                    else:
                        purple = False
                        print('紫蛇绕死了！')
                        continue
                purplemove(p2[0])
            score += 1

        if score == 50:  # 到50分加速
            cn = 3
        if score == 100:  # 到100分再加速
            cn = 2
        count += 1

        clear()
        write(score, font=('Arial', 12))
        pressKeys()
        update()
        sleep(.03)  # 动画更新速度（单位：秒）

    s[a].fillcolor('yellow')
    update()
    print('被吃到了哇！')
    sleep(1)
    done()
else:
    print("输入错了哦~")