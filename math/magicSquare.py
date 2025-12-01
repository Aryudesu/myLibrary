class magicSquare:
    def _makeOdd(self, num: int):
        result = [[0] * num for _ in range(num)]
        y, x = 0, (num - 1) // 2
        for i in range(1, num * num + 1):
            result[y][x] = i
            y = (y - 1) % num
            x = (x + 1) % num
            if result[y][x] != 0:
                y = (y + 2) % num
                x = (x - 1) % num
        return result

    def _make4Time(self, num: int):
        result = [[0] * num for _ in range(num)]
        y, x = 0, 0
        for i in range(1, num * num + 1):
            if ((y % 4) * 4 + (x % 4)) % 5 == 0 or ((y % 4) * 4 + (x % 4)) % 3 == 0:
                result[y][x] = i
            x += 1
            if x == num:
                x = 0
                y += 1
        y, x = num - 1, num - 1
        for i in range(1, num * num + 1):
            if result[y][x] == 0:
                result[y][x] = i
            x -= 1
            if x == -1:
                x = num - 1
                y -= 1
        return result

    def _lux(self, num: int):
        hnum = num // 2
        od = self._makeOdd(hnum)
        for y in range(hnum):
            for x in range(hnum):
                od[y][x] = (od[y][x] - 1) * 4
        lux = [[""] * hnum for _ in range(hnum)]
        for y in range(hnum):
            for x in range(hnum):
                if y <= (hnum - 1) // 2:
                    lux[y][x] = "L"
                elif y == (hnum - 1) // 2 + 1:
                    lux[y][x] = "U"
                else:
                    lux[y][x] = "X"
        lux[(hnum - 1) // 2][(hnum - 1) // 2] = "U"
        lux[(hnum - 1) // 2 + 1][(hnum - 1) // 2] = "L"
        result = [[0] * num for _ in range(num)]
        for y in range(hnum):
            for x in range(hnum):
                if lux[y][x] == "L":
                    result[2 * y][2 * x] = od[y][x] + 4
                    result[2 * y][2 * x + 1] = od[y][x] + 1
                    result[2 * y + 1][2 * x] = od[y][x] + 2
                    result[2 * y + 1][2 * x + 1] = od[y][x] + 3
                elif lux[y][x] == "U":
                    result[2 * y][2 * x] = od[y][x] + 1
                    result[2 * y][2 * x + 1] = od[y][x] + 4
                    result[2 * y + 1][2 * x] = od[y][x] + 2
                    result[2 * y + 1][2 * x + 1] = od[y][x] + 3
                elif lux[y][x] == "X":
                    result[2 * y][2 * x] = od[y][x] + 1
                    result[2 * y][2 * x + 1] = od[y][x] + 4
                    result[2 * y + 1][2 * x] = od[y][x] + 3
                    result[2 * y + 1][2 * x + 1] = od[y][x] + 2
        return result

    def make(self, num: int):
        if num == 1:
            return [[1]]
        if num == 2:
            return None
        if num % 2 == 1:
            return self._makeOdd(num)
        if num % 4 == 0:
            return self._make4Time(num)
        if num % 4 == 2:
            return self._lux(num)

    def draw(self, data):
        if data is None:
            return
        num = len(data)
        maxLen = len(str(num * num))
        for y in range(num):
            for x in range(num):
                print(f"[{str(data[y][x]).rjust(maxLen)}]", end="")
            print()


ms = magicSquare()
N = int(input())
ms.draw(ms.make(N))
