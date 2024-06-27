#pathfinding.py
global a, flag, tp,  b, s,sp, gap, q, p, w0, f0
def GameGraph():
    global a, flag, tp, b, s, sp,gap, q, p, w0, f0
    a = 45
    flag = 1
    tp = []
    b = [44, 45]
    sp=0.02
    s = []
    gap = []
    q = []
    p = []
    w0 = []
    f0 = []
    for i in range(100):
        w0.append(2)
        f0.append(-1)
    return a, flag, tp, b, s,sp, gap, q, p, w0, f0
def pathfinding(start,end,wew):
    def detect(n, w, q):  # 参数n代表需要检查的格子的序号；w和q不是全局变量所以要加一下
        global flag
        if w[n] == 1:  # 找到终点
            flag = 1
            return 1
        elif w[n] == 2:  # 空格子
            w[n] = 0
            q.append(n)
            return 2
    if wew=='rBFS':
        w = w0.copy()
        f = f0.copy()
        for i in b:
            w[i] = 0
        w[end] = 1  # 标记终点
        q = [start]  # 队列初始化，加入蛇头
        while q:
            v = q[0]
            if v % 2:  # 在偶数列，向上搜索
                if v < 90:
                    d = detect(v + 10, w, q)
                    if d == 1:
                        break
                    elif d == 2:
                        f[v + 10] = v
            else:  # 在奇数列，向下搜索
                if v > 9:
                    d = detect(v - 10, w, q)
                    if d == 1:
                        break
                    elif d == 2:
                        f[v - 10] = v
            if (v // 10) % 2:  # 在奇数行，向左搜索
                if v % 10 != 0:
                    d = detect(v - 1, w, q)
                    if d == 1:
                        break
                    elif d == 2:
                        f[v - 1] = v
            else:
                if v % 10 != 9:
                    d = detect(v + 1, w, q)
                    if d == 1:
                        break
                    elif d == 2:
                        f[v + 1] = v
            q.pop(0)
        while v != start:
            p.insert(0, v)
            v = f[v]
    elif wew=='tBFS':
        tb = tp[-len(b):]
        tw = w0.copy()
        for i in tb:
            tw[i] = 0
        tw[end] = 1
        q = [start]
        while q:
            v = q[0]
            if v % 2:  # 在偶数列，向上搜索
                if v < 90:
                    d = detect(v + 10, tw, q)
                    if d == 1:
                        break
            else:  # 在奇数列，向下搜索
                if v > 9:
                    d = detect(v - 10, tw, q)
                    if d == 1:
                        break
            if (v // 10) % 2:  # 在奇数行，向左搜索
                if v % 10 != 0:
                    d = detect(v - 1, tw, q)
                    if d == 1:
                        break
            else:
                if v % 10 != 9:
                    d = detect(v + 1, tw, q)
                    if d == 1:
                        break
            q.pop(0)
    return flag
