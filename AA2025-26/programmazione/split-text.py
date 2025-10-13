import os

folder = "/Users/Flint/Data/narrative/"
text_file = "promessi_sposi_raw.txt"

with open(os.path.join(folder, text_file), 'r') as infile:
    content = infile.read()

chunks = content.split("\n\n\n\n")

for i, chunk in enumerate(chunks):
    filename = f"chunk-{i}.txt"
    print(f"Writing {filename}")
    with open(os.path.join(folder, filename), 'w') as out:
        out.write(chunk)