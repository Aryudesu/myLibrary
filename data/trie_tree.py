class TrieNode:
    """Trie木のノード"""

    def __init__(self):
        self.children = {}
        # 文字列終了のノードか
        self.is_end_of_word = False
        # TODO やりたいことによってもたせるデータを用意する


class Trie:
    """Trie木"""

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

    def dfs(self, node: TrieNode | None):
        """深さ優先探索（木DP）"""
        if node is None:
            node = self.root
        for c in node.children:
            self.dfs(node.children[c])


N = int(input())
S = input().split()
trie = Trie()
for s in S:
    trie.insert(s)
trie.dfs(None)
