import numpy as np

class Hangmann:
    
    def __init__(self, 
                player_name: str, 
                word_to_guess: str = None,
                words: list = None,
                k: int = 10,
                c: int = 1,
                w: int = 3,
                v: int = 10):
        self.k = k
        self.c = c
        self.w = w
        self.v = v
        self.player_name = player_name
        self.score = self.k
        self.history = []
        if word_to_guess is None:
            self.word_to_guess = self.generate_word(words)
        else:
            self.word_to_guess = word_to_guess
        self.current_guess = "." * len(self.word_to_guess)
    
    def generate_word(self, words: list):
        if words is None:
            raise Exception('Serve una lista di parole')
        else:
            return np.random.choice(words)
        
    def ask_action(self):
        answer = input("Scegli L o P")
        return answer
    
    def get_char_guess(self):
        character = input("Scegli una lettera")
        guess = ""
        for i, x in enumerate(self.word_to_guess):
            if character == x:
                guess += character
            else:
                guess += self.current_guess[i]
        self.history.append(('L', character, self.score))
        self.score -= self.c
        self.current_guess = guess
        
    def guess_word(self):
        win = False
        word = input("Scegli una parola")
        self.history.append(('P', word, self.score))
        if word == self.word_to_guess:
            self.score += self.v
            win = True
        else:
            self.score -= self.w
        return win
    
    def play(self):
        c = 0
        while True:
            c += 1
            print(self.current_guess, "punteggio: {}".format(self.score))
            action = self.ask_action()
            if action == 'L':
                self.get_char_guess()
            elif action == 'P':
                win = self.guess_word()
                if win:
                    print("Hai vinto con {} punti".format(
                        self.score))
                    break
            else:
                pass
            if c > 1000 or self.score <= 0:
                print("Hai perso, la parola era {}".format(
                    self.word_to_guess))
                break
            
    def print_player(self):
        print(self.player_name)
        print("Punteggio: {}".format(self.score))
        
        
