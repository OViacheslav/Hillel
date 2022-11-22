LONG_TEXT = """asdlknfasldkmfasdfasdf"""
list_of_words = []


def add_word(word):
    list_of_words.append(word)
    list_of_words.sort()


def get_words(chars='', amount_of_words=5):
    if chars == '':
        return list_of_words[:amount_of_words]
    indexes_of_chars = len(chars)
    return_list = []
    for word in list_of_words:
        if len(return_list) == amount_of_words:
            return return_list
        if chars == word[:indexes_of_chars]:
            return_list.append(word)
    return return_list


def crop_text(length):
    result = ''
    start_index = 0
    last_index = length
    max_index = len(LONG_TEXT)
    while last_index < max_index:
        yield LONG_TEXT[start_index:last_index]
        start_index += length
        last_index += length
    return LONG_TEXT[start_index:]


if __name__ == '__main__':
    assert get_words('') == []

    add_word('bat')
    add_word('batman')

    assert get_words('') == ['bat', 'batman']
    assert get_words('bat') == ['bat', 'batman']
    assert get_words('batm') == ['batman']
    assert get_words('x') == []

    add_word('bar')
    add_word('bartender')
    add_word('basket')
    add_word('band')

    assert get_words('ba') == ['band', 'bar', 'bartender', 'basket', 'bat']

    text_generator = crop_text(10)
    assert next(text_generator) == "asdlknfasl"
    assert next(text_generator) == "dkmfasdfas"
    assert next(text_generator) == "df"