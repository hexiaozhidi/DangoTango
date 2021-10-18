import random


class Question:
    def __init__(self, target, book, mode):
        self.target = target
        self.book = book
        self.mode = self.pick_random_mode() if mode == -1 else mode

        self.distractors = book.pick_n_random_tangos(4)
        assert self.distractors, "词库的单词量少于4，无法出题！"
        duplicate = -1
        for i in range(4):
            if self.distractors[i] == self.target:
                duplicate = i
        self.distractors.pop(duplicate)

        if self.mode == 0:  # 已知word，求explanation
            self.message = '「%s」在汉语里的意思是下面的哪一项呢？' % self.target.word
            self.message_core = '「%s」' % self.target.word
            self.choices = [self.target.explanation] + [tango.explanation for tango in self.distractors]
        elif self.mode == 1:  # 已知explanation，求word
            self.message = '「%s」是下面哪一项的汉语意思呢？' % self.target.explanation
            self.message_core = '「%s」' % self.target.explanation
            self.choices = [self.target.word] + [tango.word for tango in self.distractors]
        elif self.mode == 2:  # 已知kana，求explanation
            self.message = '「%s」在汉语里的意思是下面的哪一项呢？' % self.target.kana
            self.message_core = '「%s」' % self.target.kana
            self.choices = [self.target.explanation] + [tango.explanation for tango in self.distractors]
        elif self.mode == 3:  # 已知explanation，求kana
            self.message = '「%s」是下面哪一项的汉语意思呢？' % self.target.explanation
            self.message_core = '「%s」' % self.target.explanation
            self.choices = [self.target.kana]
            for tango in self.distractors:
                self.choices.append(tango.kana if tango.kana else tango.word)
        elif self.mode == 4:  # 已知word，求kana
            self.message = '「%s」的另一种写法是下面的哪一项呢？' % self.target.word
            self.message_core = '「%s」' % self.target.word
            self.choices = [self.target.kana]
            for tango in self.distractors:
                self.choices.append(tango.kana if tango.kana else tango.word)
        else:  # 已知kana，求word
            self.message = '「%s」的另一种写法是下面的哪一项呢？' % self.target.kana
            self.message_core = '「%s」' % self.target.kana
            self.choices = [self.target.word] + [tango.word for tango in self.distractors]

        self.answer = self.choices[0]
        random.shuffle(self.choices)
        self.my_answer = ''

    def __str__(self):
        return self.message + '\n(A) %s\n(B) %s\n(C) %s\n(D) %s' % tuple(self.choices)

    def pick_random_mode(self):
        if not self.target.kana:
            return random.randint(0, 1)
        else:
            return random.randint(0, 5)

    def make_choice(self, my_answer):
        self.my_answer = my_answer
        self.target.update_memory()

    def check(self):
        result = self.my_answer == self.answer
        if not result:
            self.target.update_mistake()
        self.book.save_to_csv()
        return result
