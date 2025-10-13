import numpy as np

def user_input(valid_options):
    opt = " / ".join([str(x) for x in valid_options])
    error = True
    while error:
        iu = input(f"Scegli fra {opt}\n")
        error = not iu in valid_options
        if error:
            print(f"Ho detto {opt}!!!!")
        else:
            pass
    return iu

class UniformPlayer:
    def __init__(self, valid_options):
        self.vo = valid_options
        self.record_track = []
    def play(self):
        return np.random.choice(self.vo)
    def store_result(self, outcome):
        self.record_track.append(outcome)
