class SimpleFileManager:
    """簡単にファイルの読み書きを行うためのクラス"""
    
    def __init__(self, filepath, encoding='utf-8'):
        self.filepath = filepath
        self.encoding = encoding

    def write(self, content):
        """ファイルに上書きで書き込み"""
        with open(self.filepath, 'w', encoding=self.encoding) as f:
            f.write(content)

    def append(self, content):
        """ファイルに追記"""
        with open(self.filepath, 'a', encoding=self.encoding) as f:
            f.write(content)

    def read(self):
        """ファイルの内容を読み込んで返す"""
        with open(self.filepath, 'r', encoding=self.encoding) as f:
            return f.read()

    def readlines(self):
        """ファイルを行ごとに読み込んでリストで返す"""
        with open(self.filepath, 'r', encoding=self.encoding) as f:
            return f.readlines()

    def overwrite_lines(self, lines: list[str]):
        """行単位でリストを渡して上書き"""
        with open(self.filepath, 'w', encoding=self.encoding) as f:
            f.writelines(lines)
