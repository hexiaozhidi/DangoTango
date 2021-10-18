import csv
import os
import random
from datetime import datetime as dt

from Tango import Tango


class Book:
    def __init__(self, book_name):
        self.title = book_name
        self.size = 0
        self.tango_list = []
        self.tango_dict = {}
        path = 'books/%s.csv' % book_name
        if os.path.exists(path):
            self.load_from_csv(path)

    def __str__(self):
        return '单词表「%s」（收录单词数：%d）' % (self.title, self.size)

    def load_from_csv(self, path):
        _, file_name = os.path.split(path)
        file_name, _ = os.path.splitext(file_name)
        self.title = file_name
        with open(path, newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.add_tango(*row[1: 7], tango_id=int(row[0]), memory_counter=int(row[7]),
                               mistake_counter=int(row[8]), last_memory_time=row[9])

    def save_to_csv(self, path=None):
        if not path:
            path = ('books/%s.csv' % self.title)
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['tango_id', 'word', 'kana', 'english', 'tone', 'part', 'explanation',
                             'memory_counter', 'mistake_counter', 'last_memory_time'])
            for tango in self.tango_list:
                writer.writerow(self.tango_dict[tango].get_row_for_csv())

    def add_tango(self, word, kana, english, tone, part, explanation,
                  tango_id=-1, memory_counter=0, mistake_counter=0, last_memory_time=''):
        if not explanation or word in self.tango_dict:
            return
        if tango_id == -1:  # 添加新单词
            tango_id = self.size
            last_memory_time = dt.fromtimestamp(0).isoformat()
        self.tango_list.append(word)
        self.tango_dict[word] = Tango(tango_id, word, kana, english, tone, part, explanation,
                                      memory_counter, mistake_counter, last_memory_time)
        self.size += 1

    def sort_by_kana(self):
        self.tango_list.sort(key=lambda t: self.tango_dict[t])
        for i in range(self.size):
            self.tango_dict[self.tango_list[i]].update_tango_id(i)

    def sort_for_task(self, key):  # 为生成任务，将单词排序。不更新tango_id。
        def helper(t):
            tango = self.tango_dict[t]
            mistake_rate = tango.mistake_counter / tango.memory_counter if tango.memory_counter > 0 else 0
            last_memory_time = dt.fromisoformat(tango.last_memory_time)
            if key == 'mistake_rate':  # 按错误率由高到低排序，相等时按上次记忆时间由早到晚排序。
                return -mistake_rate, last_memory_time
            if key == 'last_memory_time':  # 按上次记忆时间由早到晚排序，相等时按错误率由高到低排序。
                return last_memory_time, -mistake_rate
            raise Exception('Invalid key!')

        self.tango_list.sort(key=helper)

    def preview(self, n=5):
        print(self)
        for i in range(n if self.size > n else self.size):
            tango = self.tango_dict[self.tango_list[i]]
            print('# %05d　%s' % (tango.tango_id, tango))
        if self.size > n:
            print('...')

    def pick_n_random_tangos(self, n):
        if self.size < n:
            return []
        return [self.tango_dict[t] for t in random.sample(self.tango_list, n)]
