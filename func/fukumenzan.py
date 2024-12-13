from itertools import permutations

def str2num(S, SD, TPL):
    res = 0
    num = {str(l) for l in range(10)}
    for s in S:
        if s in num:
            res = res * 10 + int(s)
        else:
            res = res * 10 + TPL[SD[s]]
    return res


def is_unsatis(un_zeros, sd, tpl):
    for uz in un_zeros:
        if tpl[sd[uz]] == 0:
            return True
    return False


def input_str(mes = "input > "):
    while True:
        print(mes, end="")
        res = input()
        if len(res.split()) == 1:
            break
    return res


def input_operator(mes = "input '+' or '*'  > "):
    """符号入力"""
    while True:
        print(mes, end="")
        res = input()
        if res == '+' or res == '*':
            break
    return res


def input_num(mes = "InputNum > "):
    """数値入力"""
    while True:
        try:
            print(mes, end="")
            return int(input())
        except Exception:
            print("this is not number")


def input_data(N):
    data = []
    un_zeros_set = set()
    chset = set()
    for n in range(N+1):
        S = input_str()
        un_zeros_set.add(S[0])
        chset.update(list(S))
        data.append(S)
    chlist = list(chset)
    chd = dict()
    un_zeros = list(un_zeros_set)
    chl = len(chlist)
    for idx in range(chl):
        chd[chlist[idx]] = idx
    return data, chl, chd, un_zeros


def display_results(N, operator, data, result):
    ld = 0
    for dat in data:
        ld = max([ld, len(dat)])
    for n in range(N):
        tmp = str(result[n]).rjust(ld, " ")
        if n:
            tmp = operator + ")" + tmp
        else:
            tmp = "  " + tmp
        print(tmp)
    print("-" * (ld + 2))
    print(str(result[-1]).rjust(ld + 2, " "))


def calc(data, chl, chd, un_zeros, operator='+'):
    # ぶん回す
    for itr in permutations(nums, chl):
        if is_unsatis(un_zeros, chd, itr):
            continue
        numl = []
        for dat in data:
            numl.append(str2num(dat, chd, itr))
        if operator == '+':
            res = 0
            for n in range(N):
                res += numl[n]
            if res == numl[-1]:
                return numl
        elif operator == '*':
            res = 1
            for n in range(N):
                res *= numl[n]
            if res == numl[-1]:
                return numl
    return None


"""計算させる数の個数"""
N = input_num()
operator = input_operator()
nums = list(range(10))
data, chl, chd, un_zeros = input_data(N)

if chl > 10:
    print("UNSOLVABLE")
else:
    numl = calc(data, chl, chd, un_zeros, operator)
    if numl is None:
        print("UNSOLVABLE")
    else:
        display_results(N, operator, data, numl)