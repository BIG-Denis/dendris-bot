
def make_uniq():
    with open('source.txt', 'r') as file:
        messages = list(set(string for string in file if string != '\n'))
    with open('source.txt', 'w') as file:
        file.writelines(messages)

    with open('img_sources.txt', 'r') as file:
        imgs = list(set(string for string in file if string != '\n'))
    with open('img_sources.txt', 'w') as file:
        file.writelines(imgs)


make_uniq()
