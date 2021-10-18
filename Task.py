import random

from Book import Book
from Question import Question


class Task:
    def __init__(self, book_name, target_num, mode_factor, revision_factor):
        self.book = Book(book_name)
        self.target_num = target_num
        self.mode_factor = mode_factor  # 题型系数，对于一个单词，需要出多少种不同类型的题
        self.revision_factor = revision_factor  # 复习系数，本次任务中的历史错误率高的单词的出现百分比，范围为0~100

        self.book.sort_for_task('mistake_rate')
        self.targets = self.book.tango_list[:int(self.target_num * self.revision_factor / 100)]
        self.book.sort_for_task('last_memory_time')
        for tango in self.book.tango_list:
            if len(self.targets) >= self.target_num:
                break
            if tango in self.targets:
                continue
            self.targets.append(tango)

        self.questions = []
        for t in self.targets:
            target = self.book.tango_dict[t]
            modes = range(6) if target.kana else [0, 0, 0, 1, 1, 1]
            for mode in random.sample(modes, self.mode_factor):
                self.questions.append(Question(target, self.book, mode))
        random.shuffle(self.questions)

        self.question_num = len(self.questions)
        self.current_question = None
        self.memory_counter = 0
        self.mistake_counter = 0

    def start_question(self):
        self.current_question = self.questions[self.memory_counter]

    def finish_question(self, result):
        if not result:
            self.mistake_counter += 1
        self.memory_counter += 1

    def get_accuracy(self):
        return (self.memory_counter - self.mistake_counter) / self.memory_counter if self.memory_counter > 0 else 0

    def get_progress(self):
        return self.memory_counter / self.question_num
