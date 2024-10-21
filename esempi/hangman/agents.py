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
        