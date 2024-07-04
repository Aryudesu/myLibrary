class trie_tree():
    """
    Trie木

    -----
    Created By Aryu
    """

    def __init__(self) -> None:
        self.tree = dict()

    def insert(self, value) -> None:
        """
        文字列データを追加します

        parameter
        -----
        value: string

        response
        -----
        None
        """
        graph = self.tree
        for v in value:
            tmp = graph.get(v, {})
            graph[v] = tmp
            cost = tmp.get("num", 0)
            tmp["num"] = cost + 1
            graph = tmp
        graph["end"] = True

    def get_max_lcp(self, value) -> None:
        """
        LCPの最大値を取得します

        parameter
        -----
        value: string

        response
        -----
        int
        """
        graph = self.tree
        result = 0
        for v in value:
            tmp = graph.get(v, {})
            num = tmp.get("num", 0)
            if num <= 1:
                break
            result += 1
            graph = tmp
        return result


# *** Example (ABC387 E) ***
tt = trie_tree()
N = int(input())
S = []
for n in range(N):
    s = input()
    S.append(s)
    tt.insert(s)
for s in S:
    res = tt.get_max_lcp(s)
    print(res)
