def read_words(file_path):
    infile = open(file_path, 'r')
    content = infile.read()
    words = content.split('\n')
    del(words[-1])
    return words 

def print_template(word, marker="_ "):
    return marker * len(word)