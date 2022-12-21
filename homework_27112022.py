WORDS = {}


def flatten(arr):
    flatten_list = []
    for elem in arr:
        flatten_list.extend(elem)
    yield from flatten_list


def grep(pattern):
    text = None
    while True:
        if isinstance(text, str) and text.find(pattern) == -1:
            text = None
        text = yield text


def get_words(chars):
    words_gatherer = ''
    index = 0
    cropped_brunch = WORDS.copy()
    checker = []
    for elem in WORDS:
        if elem == chars[index]:
            checker.append(elem)
    deep_checker = cropped_brunch.get(chars[index])
    deep_checker = str(deep_checker)
    if len(checker) == 0 or deep_checker.find(chars) == -1:
        checker = []
        return checker
    checker = []
    while index != len(chars):
        cropped_brunch = cropped_brunch.get(chars[index])
        index += 1
    string_brunch = str(cropped_brunch)
    if string_brunch.find('TERM') < 0:
        return checker
    string_brunch = string_brunch[string_brunch.find('TERM'):]
    string_brunch2 = ''
    for i in string_brunch:
        if i != "'" and i != ':' and i != '{' and i != '}':
            string_brunch2 += i
    string_cleaner = string_brunch2.replace('TERM', '').strip()
    string_cleaner += ','
    for elem in string_cleaner:
        if elem != ',' and elem != ' ':
            words_gatherer += elem
        if elem == ',':
            checker.append(words_gatherer)
            words_gatherer = ''
    index_final = 0
    for elem in checker:
        if elem[:len(chars)] != chars:
            while elem[index_final:len(chars) + index_final] != chars:
                index_final += 1
            if elem[index_final:len(chars) + index_final] == chars:
                checker.append(elem[index_final:])
                print(elem)
                print(elem[index_final:len(chars)])
                checker.remove(elem)
                return checker
    return checker


def add_word(word):
    length_of_word = len(word)
    temp_dict = {'TERM': word}
    for symbol in word[::-1]:
        temp_dict = {symbol: temp_dict}
    searcher = []
    for key in WORDS:
        if key == word[0]:
            searcher.append(key)
    if not searcher:
        WORDS.update(temp_dict)
        return WORDS
    pos_in_dict = []
    index = 0
    second_temp_dict = WORDS.get(searcher[0])
    str_temp_dict = str(second_temp_dict)
    dict_brunch_diver = str_temp_dict.find(word)
    for i in word:
        pos_in_dict.append(i)
    dict_diver = ""
    while length_of_word > index:
        dict_diver += ".get(pos_in_dict[" + str(index) + "])"
        index += 1
    if dict_brunch_diver > 0:
        if searcher == [word[0]]:
            for elem in WORDS:
                if elem == pos_in_dict[0]:
                    dict_diver += ".setdefault('TERM', word)"
                    result_dict = 'WORDS' + dict_diver
                    exec(result_dict)
                    return WORDS
    while get_words(word[:length_of_word]) == []:
        length_of_word -= 1
    index = 1
    cropped_brunch = WORDS.get(pos_in_dict[0])
    temp_dict = temp_dict.get(pos_in_dict[0])
    while index < length_of_word:
        cropped_brunch = cropped_brunch.get(pos_in_dict[index])
        temp_dict = temp_dict.get(pos_in_dict[index])
        index += 1
    if index == length_of_word:
        temp_dict = temp_dict.get(pos_in_dict[index])
        cropped_brunch.setdefault(pos_in_dict[index], temp_dict)
    return WORDS




if __name__ == '__main__':
    assert list(flatten([])) == []
    assert list(flatten([[]])) == []
    assert list(flatten([[], []])) == []
    assert list(flatten([[1, 2], [], [3]])) == [1, 2, 3]
    assert list(flatten([[1, 2], [3, 4, 5]])) == [1, 2, 3, 4, 5]

    search = grep('bbq')
    next(search)
    assert search.send('Birthday invitation') is None
    assert search.send('Bring bbq sauce with') == 'Bring bbq sauce with'
    assert search.send('Are you hungry?') is None
    assert search.send("We won't invite you to our BBQ party then") is None
    assert search.send('but you better be quick (bbq) otherwise') == 'but you better be quick (bbq) otherwise'
    search.close()

    add_word('hello')
    assert WORDS == {'h': {'e': {'l': {'l': {'o': {'TERM': 'hello'}}}}}}
    add_word('hell')
    assert WORDS == {'h': {'e': {'l': {'l': {'o': {'TERM': 'hello'}, 'TERM': 'hell'}}}}}
    add_word('he')
    assert WORDS == {'h': {'e': {'l': {'l': {'o': {'TERM': 'hello'}, 'TERM': 'hell'}}, 'TERM': 'he'}}}
    # set is used here to ignore order but not to remove duplicates
    # the task doesn't require words to be in specific order
    assert set(get_words('he')) == {'he', 'hell', 'hello'}
    assert get_words('l') == []
    assert set(get_words('hel')) == {'hell', 'hello'}
