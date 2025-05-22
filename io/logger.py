import sys


class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        if not self.log.closed:
            self.log.write(message)

    def flush(self):
        self.terminal.flush()
        if not self.log.closed:
            self.log.flush()

    def close(self):
        if not self.log.closed:
            self.log.close()


# sys.stdout を差し替え
sys.stdout = Logger("output.log")

# これで print するだけで標準出力とファイル両方に出力される
print("Hello, world!")
print("これはログファイルにも書き込まれます")

# 最後に明示的に閉じる場合（ただし通常はファイルは自動で閉じられる）
sys.stdout.close()
