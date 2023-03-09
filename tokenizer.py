import re
import os
import pymorphy2
from nltk.stem import WordNetLemmatizer

from nltk import word_tokenize
from nltk.corpus import stopwords
from pymystem3 import Mystem

directory = 'output'


# that directory


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


def lemmatize(tokens):
    mystem = Mystem()
    tokens = [token.replace(token, ''.join(mystem.lemmatize(token))) for token in tokens]
    return tokens


morph = pymorphy2.MorphAnalyzer()

if __name__ == '__main__':
    i = 0
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(f)
        with open(f, 'r', encoding='utf-8') as file:
            text = file.read()
            tokens = token_text(text)
            clean_toks = remove_stop_words(tokens)
            lemmatizer = WordNetLemmatizer()
            with open(f"tokens.txt", 'w', encoding='utf-8') as output_file:
                output_file.writelines("%s\n" % i for i in clean_toks)
                output_file.close()

            lemma_mapping = dict()
            for token in clean_toks:
                parsed_token = morph.parse(token)[0]
                token_lemma = parsed_token.normal_form
                if token_lemma not in lemma_mapping.keys():
                    lemma_mapping[token_lemma] = [token]
                else:
                    lemma_mapping[token_lemma].append(token)

            # writing lemmas
            with open('lemmas.txt', mode='w', encoding='utf-8') as lemmas:
                for key, values in lemma_mapping.items():
                    lemmas.write(f'{key}  :  {" ".join(values)}\n')


        i = i + 1
print(lemmatize(clean_toks))
