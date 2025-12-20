import sys
sys.setrecursionlimit(10**6)

class TrieNode:
    """Trie木のノード"""
    __slots__ = ("children", "labels")
    def __init__(self):
        self.children = {}
        self.labels = []
        # TODO やりたいことによってもたせるデータを用意する

class AppendTrieTree:
    """末尾追加型のTrie木"""
    def __init__(self, rootLabel: str|int = "root"):
        self.root = TrieNode()
        self.nodes = {rootLabel: self.root}
    
    def append(self, prev, val, label):
        """
        prevに対しvalをキーとしたlabelのついたノードを追加します
        valをキーとしたノードが存在する場合は，対象のノードにキーを追加します．
        """
        assert prev in self.nodes
        prevNode = self.nodes[prev]
        nextNode = prevNode.children.get(val)
        if nextNode is None:
            nextNode = TrieNode()
            prevNode.children[val] = nextNode
        nextNode.labels.append(label)
        self.nodes[label] = nextNode

# === Sample: ABC437E
# 辞書順にデータを取得します
def dfs(root: TrieNode):
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        node.labels.sort()
        result.extend(node.labels)
        keys = sorted(node.children.keys(), reverse=True)
        for k in keys:
            stack.append(node.children[k])
    return result

at = AppendTrieTree(0)
N = int(input())
for n in range(1, N + 1):
    x, y = map(int, input().split())
    at.append(x, y, n)
g = at.root
result = dfs(g)
print(*result)
