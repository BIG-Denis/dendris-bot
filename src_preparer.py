
def make_uniq():
    with open('res/source.txt', 'r') as file:
        messages = list(set(string for string in file if string != '\n'))
    with open('res/source.txt', 'w') as file:
        file.writelines(messages)

    with open('res/img_sources.txt', 'r') as file:
        imgs = list(set(string for string in file if string != '\n'))
    with open('res/img_sources.txt', 'w') as file:
        file.writelines(imgs)


if __name__ == '__main__':
    make_uniq()
