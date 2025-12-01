class CuttableList:
    """
    切断可能な配列管理用クラス
    同じ要素が2度使われないことが保証されていること前提
    """

    def __init__(self, Data = []):
        self.array_data = dict()

    def join(self, x, y):
        """xの後にyを結合します"""
        x_data = self.array_data.get(x, dict())
        assert x_data.get("next") is None
        y_data = self.array_data.get(y, dict())
        assert y_data.get("prev") is None
        x_data["next"] = y
        y_data["prev"] = x
        self.array_data[x] = x_data
        self.array_data[y] = y_data

    def cut(self, x, y):
        """xとyを分離します"""
        x_data = self.array_data.get(x, dict())
        y_data = self.array_data.get(y, dict())
        x_data["next"] = None
        y_data["prev"] = None
        self.array_data[x] = x_data
        self.array_data[y] = y_data

    def get_array(self, a):
        """aが属するグループを配列で取得します"""
        data = self.array_data.get(a, dict())
        now_a = a
        while True:
            prev = data.get("prev")
            if prev is None:
                break
            now_a = prev
            data = self.array_data.get(now_a, dict())
        result = []
        data = self.array_data.get(now_a, dict())
        while True:
            result.append(now_a)
            next = data.get("next")
            if next is None:
                break
            now_a = next
            data = self.array_data.get(now_a, dict())
        return result


# # *** Example (ABC225 D) ***
cl = CuttableList()
N, Q = [int(l) for l in input().split()]
for q in range(Q):
    num, *query = [int(l) for l in input().split()]
    if num == 1:
        x, y = query
        cl.join(x, y)
    elif num == 2:
        x, y = query
        cl.cut(x, y)
    else:
        x = query[0]
        res = cl.get_array(x)
        print(len(res), *res)
