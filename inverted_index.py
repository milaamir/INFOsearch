from os import walk
import re
import nltk
import pymorphy2

from nltk.stem import WordNetLemmatizer

from nltk import word_tokenize
from nltk.corpus import stopwords
from pymystem3 import Mystem

invalid_poses = ['CONJ', 'PREP']
inverted_index = dict()

morph = pymorphy2.MorphAnalyzer()


def lemmatize(tokens):
    mystem = Mystem()
    tokens = [token.replace(token, ''.join(mystem.lemmatize(token))) for token in tokens]
    return tokens


def token_text(text):
    tokens = word_tokenize(text)
    return tokens


def remove_stop_words(tokens):
    tokens = [re.sub(r"\W", "", token, flags=re.I) for token in tokens]

    stop_words = stopwords.words('russian')
    only_cyrillic_letters = re.compile('[а-яА-Я]')

    tokens = [token.lower() for token in tokens if (token not in stop_words)
              and only_cyrillic_letters.match(token)
              and not token.isdigit()
              and token != '']

    return tokens
#
# def intersection(lst1, lst2):
#     lst3 = [value for value in lst1 if value in lst2]
#     return lst3

if __name__ == '__main__':
    def update_inverted_index(index_map, array, value):
        for elem in array:
            if elem not in index_map.keys():
                index_map[elem] = [value]
            else:
                index_map[elem].append(value)


    # getting tokens
    filenames = next(walk('output/'), (None, None, []))[2]
    for filename in filenames:
        with open('output/' + filename, mode='r', encoding='utf-8') as file:
            cleaned_tokens = []
            text = file.read()
            tokens = token_text(text)
            page_tokens = remove_stop_words(tokens)
            for token in page_tokens:
                if not any([letter.isdigit() for letter in token]) or r'//' in token:
                    parsed_token = morph.parse(token)[0]
                    if parsed_token.tag.POS and parsed_token.tag.POS not in invalid_poses:
                        cleaned_tokens.append(token)
            cleaned_tokens = set(cleaned_tokens)
            value = filename.split('.')[0]
            update_inverted_index(inverted_index, cleaned_tokens, value)

        # writing inverted index
        with open('inverted_lem_index.txt', mode='w', encoding='utf-8') as file:
            for key, values in inverted_index.items():
                print(filename)
                file.write(f'{key} {" ".join(values)}\n')