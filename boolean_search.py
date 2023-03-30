inverted_index = dict()

AND_OPERATOR = 'AND'
OR_OPERATOR = 'OR'
NOT_OPERATOR = 'NOT'


def or_operation(query_words):
    result = []
    for token in query_words:
        if inverted_index[token]:
            result.extend(inverted_index[token])
    return set(result)


def and_operator(query_words):
    pages = []
    for token in query_words:
        if token in inverted_index:
            if inverted_index[token]:
                pages.append(set(inverted_index[token]))
    if len(pages) != 0:
        result = pages[0]
        for page in pages:
            result &= page
        return result
    else:
        return 0


def not_operator(query_words):
    pp = []
    notpp = []
    pp = inverted_index[query_words[0]]
    query_words.pop(0)
    for token in query_words:
        if inverted_index[token]:
            notpp = inverted_index[token]
    for el in notpp:
        if el in pp:
            pp.remove(el)
    return pp


def search(operator, query_words):
    if operator == OR_OPERATOR:
        query_words.remove('or')
        return or_operation(query_words)
    elif operator == AND_OPERATOR:
        query_words.remove('and')
        return and_operator(query_words)
    elif operator == NOT_OPERATOR:
        query_words.remove('not')
        return not_operator(query_words)


with open('inverted_index.txt', encoding='utf-8') as input_file:
    lines = input_file.readlines()
    for line in lines:
        key = line.rstrip().split(' ')[0]
        values = line.rstrip().split(' ')[1:]
        inverted_index[key] = values

if __name__ == '__main__':
    query = input('Введите запрос:\n')
    args = query.split(' ')
    if len(args) > 1:
        operator = args[0].upper()
    else:
        operator = OR_OPERATOR

    print(search(operator, args[0:]))
