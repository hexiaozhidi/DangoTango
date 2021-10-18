from datetime import datetime as dt

from jp_tools import *


class Tango:
    def __init__(self, tango_id, word, kana, english, tone, part, explanation,
                 memory_counter, mistake_counter, last_memory_time):
        self.tango_id = tango_id
        self.word = word
        self.kana = kana
        self.english = english
        self.tone = get_tone(tone)
        self.part = get_part(part)
        self.explanation = explanation
        self.memory_counter = memory_counter
        self.mistake_counter = mistake_counter
        self.last_memory_time = last_memory_time

    def __str__(self):
        if self.kana:
            return '%s（%s）%s %s %s' % (self.word, self.kana, self.tone, self.part, self.explanation)
        if self.english:
            return '%s（%s）%s %s %s' % (self.word, self.english, self.tone, self.part, self.explanation)
        return '%s %s %s %s' % (self.word, self.tone, self.part, self.explanation)

    def __eq__(self, other):
        assert type(self) == type(other), "Wrong type for tango comparison!"
        return self.word == other.word

    def __lt__(self, other):
        assert type(self) == type(other), "Wrong type for tango comparison!"
        if self.get_hira(drop_symbol=True) < other.get_hira(drop_symbol=True):
            return True
        if self.get_hira(drop_symbol=True) > other.get_hira(drop_symbol=True):
            return False
        return self.word < other.word

    def get_hira(self, drop_symbol=False):
        hira = kata_to_hira(self.kana if self.kana else self.word)
        if drop_symbol:
            return str.join('', map(lambda h: h if h in HIRA else '', hira))
        return hira

    def update_tango_id(self, tango_id):
        self.tango_id = tango_id

    def update_memory(self):
        self.memory_counter += 1
        self.last_memory_time = dt.now().isoformat()

    def update_mistake(self):
        self.mistake_counter += 1

    def get_row_for_csv(self):
        return [self.tango_id, self.word, self.kana, self.english, self.tone, self.part, self.explanation,
                self.memory_counter, self.mistake_counter, self.last_memory_time]
