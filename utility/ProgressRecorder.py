import os
import json

class ProgressRecorder:
    """データ保存・再開が簡単になるクラス"""
    def __init__(self, filename:str='progress.json'):
        self.filename = filename
        self.state = {
            "current_index": 0,
            "found_values": []
        }
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.state = json.load(f)

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.state, f, indent=2)

    def set_index(self, index):
        self.state['current_index'] = index

    def get_index(self):
        return self.state['current_index']

    def append_value(self, value):
        self.state['found_values'].append(value)

    def get_values(self):
        return self.state['found_values']

    def clear(self):
        self.state = {
            "current_index": 0,
            "found_values": []
        }
        self.save()

pr = ProgressRecorder()
N = 10000000
for i in range(2, N):
    is_ok = True
    for j in range(2, i):
        if i % j == 0:
            is_ok = False
    if is_ok:
        pr.append_value(i)
    pr.set_index(i+1)
    if i % 100 == 0:
        pr.save()
pr.save()

