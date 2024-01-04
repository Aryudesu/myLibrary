class simpleQueue:
    def __init__(self) -> None:
        self.__payload = []
        self.__pos = 0

    def reserve(self, n):
        while len(self.__payload) < n:
            self.__payload.append(None)

    def clear(self):
        self.__payload.clear()
        self.__pos = 0

    def empty(self):
        return self.__pos == len(self.__payload)

    def push(self, x):
        self.__payload.append(x)

    def front(self):
        return self.__payload[self.__pos]

    def size(self):
        return len(self.__payload) - self.__pos

    def pop(self):
        self.__pos += 1