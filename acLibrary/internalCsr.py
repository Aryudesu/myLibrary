class csr:
    def __init__(self) -> None:
        self.__start = []
        self.__elist = []

    def csr(self, n, edges):
        self.__start = [None] * (n + 1)
        self.__elist = [None] * len(edges)
        for e in edges:
            self.__start[e[0] + 1] += 1
        for i in range(1, n + 1):
            self.__start[i] += self.__start[i-1]
        counter = self.__start
        for e in edges:
            self.__elist[counter[e[0]]] = e[1]
