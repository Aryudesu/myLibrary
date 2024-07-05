class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.total = 0

    def insert(self, word):
        """データの挿入を行います"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            self.total += node.count
            node.count += 1
        node.is_end_of_word = True

    def search(self, word):
        """データの検索を行います"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        """先頭一致でデータの取得を行います"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

N = int(input())
S = input().split()
trie = Trie()
for s in S:
    trie.insert(s)
print(trie.total)
