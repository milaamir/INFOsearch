import io
import math


def count_tf(freq, count):
    tf = freq / count
    return tf


def count_idf(frequancy):
    if frequancy != 0:
        idf = math.log(100 / frequancy)
        return idf
    else:
        return 0


def lemmas():
    frequency = {}
    with open('lemmas.txt', encoding='utf-8') as file:
        for line in file:
            words = line.split()
            count = len(words[words.index(':') + 1:])
            frequency[words[0]] = count

        for key in frequency:
            frequency[key] = count_tf(frequency[key], 1159)

    idf = {}
    with open('lemmas.txt', "r", encoding='utf-8') as text:
        for line in text:
            array_str = line.split(":", 1)[-1].strip().split()
            first_word = line.split(':')[0].strip()
            idf[first_word] = 0
            for i in range(0, 100):
                file = f"output/{i}.html"
                with open(file, "r", encoding='utf-8') as f:
                    file_contents = f.read().lower()
                    for word in array_str:
                        if word in file_contents:
                            idf[first_word] += 1
                            # print(f"Слово '{word}' найдено в файле '{file}'")
                            break
    for key in idf:
        idf[key] = count_idf(idf[key])

    for i in range(0, 100):
        with open(f"lemmas/{i}.txt", 'w', encoding="utf-8") as output_file:
            file = f"output/{i}.html"
            with open(file, "r", encoding='utf-8') as f:
                file_contents = f.read().lower()
                with open('lemmas.txt', "r", encoding='utf-8') as text:
                    for line in text:
                        array_str = line.split(":", 1)[-1].strip().split()
                        first_word = line.split(':')[0].strip()
                        for word in array_str:
                            if word in file_contents:
                                kf_idf = frequency[first_word] * idf[first_word]
                                output_file.write(f'{first_word} {frequency[first_word]} {idf[first_word]} {kf_idf}\n')
                            break
        output_file.close()


def termin():
    word_counts = {}
    with open('tokens.txt', encoding='utf-8') as file:
        for line in file:
            str = line.strip()
            if str in word_counts:
                word_counts[str] += 1
            else:
                word_counts[str] = 1

    for key in word_counts:
        word_counts[key] = count_tf(word_counts[key], 3782)
        # print(key, word_counts[key])

    idf_token = {}
    with open('tokens.txt', "r", encoding='utf-8') as text:
        for line in text:
            str = line.strip()
            for i in range(0, 100):
                file = f"output/{i}.html"
                with open(file, "r", encoding='utf-8') as f:
                    file_contents = f.read().lower()
                    if str in file_contents:
                        if str in idf_token:
                            idf_token[str] += 1
                        else:
                            idf_token[str] = 0
                        break
    for key in idf_token:
        idf_token[key] = count_idf(idf_token[key])

    for i in range(0, 100):
        with open(f"tokens/{i}.txt", 'w', encoding="utf-8") as output_file:
            file = f"output/{i}.html"
            with open(file, "r", encoding='utf-8') as f:
                file_contents = f.read().lower()
                with open('tokens.txt', "r", encoding='utf-8') as text:
                    for line in text:
                        str = line.strip()
                        if str in file_contents:
                            kf_idf = word_counts[str] * idf_token[str]
                            output_file.write(f'{str} {word_counts[str]} {idf_token[str]} {kf_idf}\n')
        output_file.close()


if __name__ == '__main__':
    # lemmas()
    termin()
