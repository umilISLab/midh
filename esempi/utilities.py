def read_words(file_path):
    infile = open(file_path, 'r')
    content = infile.read()
    words = content.split('\n')
    del(words[-1])
    return words 

def print_template(word, marker=" _ ", character="", space=True):
    template = ""
    for c in word:
        if c == character:
            if space:
                template += " {} ".format(c)
            else:
                template += c
        else:
            template += marker
    return template
            
        
