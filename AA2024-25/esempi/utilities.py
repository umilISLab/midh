def read_words(file_path):
    infile = open(file_path, 'r')
    content = infile.read()
    words = content.split('\n')
    del(words[-1])
    return words 

def print_template(word, marker=" _ ", character="", space=True, current_guess=None):
    if current_guess is None:
        current_guess = "." * len(word)
    template = ""
    for i, c in enumerate(word):
        if c == character:
            if space:
                template += " {} ".format(c)
            else:
                template += c
        else:
            g = current_guess[i]
            if g == '.':
                template += marker
            else:
                template += g
    return template

def update_guess(character, word_to_guess, current_guess):
    new_current_guess = ""
    for i, c in enumerate(word_to_guess):
        if c == character:
            new_current_guess += c
        else:
            new_current_guess += current_guess[i]
    return new_current_guess
            
        
