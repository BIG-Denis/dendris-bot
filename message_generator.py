
from random import choice, choices, randint
from src_preparer import make_uniq


def update_source():
    global messages
    make_uniq()
    with open('source.txt', 'r') as file:
        messages = [string for string in file]


def write_source(raw_source: str):
    if len(raw_source) == 1:
        return None
    res = raw_source.split(' ')
    if len(res) / len(set(res)) < 2:
        new_source = raw_source
        if len(new_source) == 1:
            return None
    else:
        return None
    # final adding
    with open('source.txt', 'a') as file:
        file.write(f'{new_source}\n')
        messages.append(new_source)


def generate_text() -> str:

    def def_len_cut(_def_text: str) -> list:
        cuts = (None, None)
        while cuts.count(None) == 2:
            cuts = choices([None, randint(1, len(_def_text))], weights=(10, 20), k=2)
        return sorted(cuts) if cuts.count(None) == 0 else cuts

    generated_message: str = ''
    res_count = (choices([1, 2, 3, 4, 5], weights=(5, 35, 50, 35, 15), k=1))[0]
    res_texts = [choice(messages)[:-1] for _ in range(res_count)]

    for text in res_texts:
        cut = (None, None)
        cut_type = (choices(['rand_len', 'rand_word', 'full'], weights=(50, 50, 50), k=1))[0]

        def def_rand_len(def_text: str) -> None:
            nonlocal cut, generated_message
            cut = def_len_cut(def_text)
            generated_message += def_text[cut[0]:cut[1]]

        def def_rand_word(def_text: str) -> None:
            nonlocal cut, generated_message
            words = def_text.split(' ')
            if len(words) > 5:
                cut = def_len_cut(def_text)
                generated_message += f' {" ".join(words[cut[0]:cut[1]])} '
            else:
                def_rand_len(def_text)

        def def_full(def_text: str) -> None:
            nonlocal generated_message
            if len(def_text) > 150:
                def_rand_word(def_text)
            else:
                generated_message += def_text

        if cut_type == 'full':
            def_full(text)
        elif cut_type == 'rand_word':
            def_rand_word(text)
        elif cut_type == 'rand_len':
            def_rand_len(text)

    if len(generated_message) < 10:
        generated_message = generate_text()

    return generated_message
