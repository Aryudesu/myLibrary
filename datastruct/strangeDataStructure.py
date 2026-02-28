from dataclasses import dataclass

class Node:
    def __init__(self, data: str=""):
        self.prevNode = None
        self.nextNode = None
        self.data = data

    def add(self, nextNode: "Node"):
        nn = self.nextNode
        if nn is not None:
            nn.prevNode = nextNode
        nextNode.nextNode = nn
        nextNode.prevNode = self
        self.nextNode = nextNode

class StrangeDataStructure:
    def __init__(self):
        self.root = Node("")
        self.center = self.root
        self.back = self.root
        self.front = self.root
        self.num = 0
    
    def append(self, data: str):
        tmp = Node(data)
        self.back.add(tmp)
        self.back = tmp
        if self.num % 2 == 0:
            self.center = self.center.nextNode
        self.num += 1
    
    def appendCenter(self, data: str):
        tmp = Node(data)
        self.center.add(tmp)
        if self.back is self.center:
            self.back = self.center.nextNode
        if self.num % 2 == 0:
            self.center = self.center.nextNode
        self.num += 1

    def popleft(self)->str:
        self.front = self.front.nextNode
        if self.num%2==0:
            self.center = self.center.nextNode
        self.num -= 1
        return self.front.data

    def getleft(self)->str:
        res = self.front.nextNode
        return res.data
    
    def debug(self):
        print("=== DEBUG ===")
        pos = self.front
        while pos.nextNode is not None:
            pos = pos.nextNode
            if pos is None:
                print(" pos is None ")
            else:
                print(pos.data)
        print("=== DEBUG ===")

result = []
sds = StrangeDataStructure()
Q = int(input())
for _ in range(Q):
    query = input().split()
    q = query[0]
    if q == "A":
        d = query[1]
        sds.append(d)
    elif q == "B":
        d = query[1]
        sds.appendCenter(d)
    elif q == "C":
        sds.popleft()
    elif q == "D":
        result.append(sds.getleft())
    else:
        raise ValueError()
    # sds.debug()
for r in result:
    print(r)
