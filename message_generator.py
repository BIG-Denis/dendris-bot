
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

    # SliceGen functions
    def def_len_cut(_def_text: str) -> list:
        cuts = (None, None)
        while cuts.count(None) == 2 or (cuts.count(None) == 0 and abs(cuts[0] - cuts[1]) < 3):
            cuts = choices([None, randint(1, len(_def_text))], weights=(10, 20), k=2)
        return sorted(cuts) if cuts.count(None) == 0 else cuts

    def def_word_cut(_def_text: str) -> list:
        words = _def_text.split(' ')
        cuts = (None, None)
        while cuts.count(None) == 2 or (cuts.count(None) == 0 and abs(cuts[0] - cuts[1]) < 2):
            cuts = choices([None, randint(1, len(words))], weights=(10, 20), k=2)
        return sorted(cuts) if cuts.count(None) == 0 else cuts

    # TextGen functions
    def def_rand_len(def_text: str, cuts: list) -> str:
        return def_text[cuts[0]:cuts[1]]

    def def_rand_word(def_text: str, cuts: list) -> str:
        words = def_text.split(' ')
        if len(words) > 5:
            return f' {" ".join(words[cuts[0]:cuts[1]])} '
        else:
            return def_rand_len(def_text, def_len_cut(def_text))

    def def_full(def_text: str) -> str:
        if len(def_text) > 150:
            return def_rand_word(def_text, def_word_cut(def_text))
        else:
            return def_text

    # Final generating text function
    def text_gen(_res_texts: list):
        _text = ''
        for text in _res_texts:
            cut_type = (choices(['rand_len', 'rand_word', 'full'], weights=(50, 50, 50), k=1))[0]
            if cut_type == 'full':
                _text += def_full(text)
            elif cut_type == 'rand_word':
                _text += def_rand_word(text, def_word_cut(text))
            elif cut_type == 'rand_len':
                _text += def_rand_len(text, def_len_cut(text))
        return _text

    # Gen parameters
    generated_message: str = ''
    res_count = (choices([1, 2, 3, 4, 5], weights=(5, 35, 50, 35, 15), k=1))[0]
    res_texts = [choice(messages)[:-1] for _ in range(res_count)]

    while len(generated_message) < 10:
        generated_message = text_gen(res_texts)

    return generated_message
