import math


def inputNum(mes="InputNum > "):
    while True:
        try:
            print(mes, end="")
            return int(input())
        except:
            print('Input "Num" Please')


def isSquare(num):
    tmp = int(math.sqrt(num))
    for i in range(-1, 2):
        if (tmp + i) ** 2 == num:
            return True
    return False


# Continued fraction expansion
def CFE(num):
    res = []
    rootnum = int(math.sqrt(num))
    ak = rootnum
    res.append(ak)
    Pk = 0
    Qk = 1
    first = True
    while True:
        Pk1 = ak * Qk - Pk
        Qk1 = (num - Pk1**2) // Qk
        if first:
            TP = Pk1
            TQ = Qk1
            first = False
        elif TP == Pk1 and TQ == Qk1:
            break
        ak = (Pk1 + rootnum) // Qk1
        Pk = Pk1
        Qk = Qk1
        res.append(ak)
    return res


def calc(CF, mode=True):
    cycle = len(CF) - 1
    if mode:
        loop = 2 * cycle - 1 if cycle % 2 else cycle - 1
    else:
        loop = cycle - 1
    pn1 = 1
    qn1 = 0
    for i in range(loop - 1, -1, -1):
        pn = CF[i % cycle + 1] * pn1 + qn1
        qn = pn1
        pn1 = pn
        qn1 = qn
    return CF[0] * pn1 + qn1, pn1


# Solve Pell Equation
def pell(num):
    if isSquare(num):
        print("Non-trivial Solution does not exist")
        return
    CF = CFE(num)
    pn, qn = calc(CF)
    print(f"({pn}, {qn})\n  {pn}*{pn} - {num} * {qn}*{qn} = 1")
    if (len(CF) - 1) % 2:
        pn, qn = calc(CF, False)
        print(f"({pn}, {qn})\n  {pn}*{pn} - {num} * {qn}*{qn} = -1")


pell(inputNum())
