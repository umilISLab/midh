from hangman import Hangmann
from abc import abstractmethod
import numpy as np
from string import ascii_lowercase

class AutomaticPlayer:
    def __init__(self, game: Hangmann):
        self.game = game 
    
    @abstractmethod
    def policy(self):
        pass
    
    @abstractmethod
    def guess_char(self):
        pass 
    
    @abstractmethod
    def guess_word(self):
        pass 
    
    @abstractmethod
    def play(self):
        pass
    
class DummyPlayer(AutomaticPlayer):
    
    def policy(self):
        return np.random.choice(['L', 'P'])
    
    def guess_char(self):
        return np.random.choice(list(ascii_lowercase))
    
    def guess_word(self):
        return np.random.choice(self.game.words)
    
    def play(self, max_iterations: int = 1000):
        for it in range(max_iterations):
            win = False
            p = self.policy()
            if p == 'L':
                c = self.guess_char()
                self.game.char_guess(character=c)
            elif p == 'P':
                w = self.guess_word()
                win = self.game.try_word(word=w)
            else:
                pass
            if win:
                return win, self.game.score 
            else:
                if self.game.score <= 0:
                    return False, self.game.score


class LessDummyPlayer(AutomaticPlayer):
    
    def __init__(self, game: Hangmann, 
                word_index: dict = None, freq: list = None,
                prob_l: float = 0.5):
        super().__init__(game=game)
        self.prob_l = prob_l
        self.asked_chars = set()
        if freq is None:
            self.freq = self.count_chars()
            self.freq = sorted([(x, y) for x, y in self.freq.items()], key=lambda x: -x[1])
        else:
            self.freq = freq
        self.word_index = {}
        if word_index is None:
            self.index_words()
        else:
            self.word_index = word_index
    
    def count_chars(self):
        freq = {}
        for word in self.game.words:
            for c in word:
                if c in freq.keys():
                    freq[c] += 1
                else:
                    freq[c] = 1
        return freq
    
    def index_words(self):
        for word in self.game.words:
            for i, c in enumerate(word):
                if c in self.word_index:
                    if i in self.word_index[c]:
                        self.word_index[c][i].append(word)
                    else:
                        self.word_index[c][i] = [word]
                else:
                    self.word_index[c] = {i: [word]}
    
    def policy(self):
        probs = np.array([self.prob_l, 1 - self.prob_l])
        return np.random.choice(['L', 'P'], p=probs)
    
    def guess_char(self):
        candidate = [(c, f) for c, f in self.freq if c not in self.asked_chars]
        char = candidate[0][0]
        self.asked_chars.add(char)
        return char
    
    def guess_word(self):
        ln = len(self.game.current_guess)
        candidates = [x for x in self.game.words if len(x) == ln]
        for i, c in enumerate(self.game.current_guess):
            if c != '.':
                k = self.word_index[c][i]
                if len(candidates) == 0:
                    candidates = k 
                else:
                    candidates = [x for x in k if x in candidates]
        return np.random.choice(candidates)
    
    def play(self, max_iterations: int = 1000):
        for it in range(max_iterations):
            win = False
            p = self.policy()
            if p == 'L':
                c = self.guess_char()
                self.game.char_guess(character=c)
            elif p == 'P':
                w = self.guess_word()
                win = self.game.try_word(word=w)
            else:
                pass
            if win:
                return win, self.game.score 
            else:
                if self.game.score <= 0:
                    return False, self.game.score
