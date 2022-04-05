
def make_uniq():
    with open('source.txt', 'r') as file:
        messages = list(set(string for string in file if string != '\n'))

    with open('source.txt', 'w') as file:
        file.writelines(messages)


make_uniq()
