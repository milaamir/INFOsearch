import math
import boolean_search


# загрузка инвертированного индекса из файла
def load_inverted_index(filename):
    inverted_index = {}
    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:
            term, *docs = line.split()
            inverted_index[term] = set(docs)
    return inverted_index


# загрузка информации о tf, idf и tf-idf из файла
def load_tf_idf(filename):
    tf = {}
    idf = {}
    tf_idf = {}
    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:
            term, tf_weight, idf_weight, tf_idf_weight = line.split()
            tf[term] = float(tf_weight)
            idf[term] = float(idf_weight)
            tf_idf[term] = float(tf_idf_weight)
    return tf, idf, tf_idf


# вычисление векторной модели документа
def compute_document_vector(tf_idf, terms):
    vector = []
    for term in terms:
        if term in tf_idf:
            vector.append(tf_idf[term])
        else:
            vector.append(0.0)
    return vector


def cosine_similarity(vector1, vector2):
    dot_product = 0
    norm1 = 0
    norm2 = 0
    for key in set(range(len(vector1))) & set(range(len(vector2))):
        dot_product += vector1[key] * vector2[key]
    norm1 = sum(value ** 2 for value in vector1)
    norm2 = sum(value ** 2 for value in vector2)
    cosine_similarity = dot_product / (math.sqrt(norm1) * math.sqrt(norm2))
    return cosine_similarity


def vector_search(query, result, tf_idf_docs):
    document_scores = {}
    for doc_id in result:
        print(doc_id)
        document_vector = [tf_idf_docs[int(doc_id)][term] if term in tf_idf_docs[int(doc_id)] else 0.1 for term in
                           query]
        print(document_vector)
        query_vector = [tf_idf_docs[int(doc_id)].get(term) if term in tf_idf_docs[int(doc_id)] else 0.1 for term in
                        query]
        print(query_vector)
        score = cosine_similarity(document_vector, query_vector)
        document_scores[doc_id] = score
    sorted_documents = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_documents


# загрузка информации о tf, idf и tf-idf для всех документов
def load_all_tf_idf(directory, prefix):
    tf_docs = {}
    idf_docs = {}
    tf_idf_docs = {}
    for i in range(100):  # здесь 10 - количество документов
        filename = directory + '/' + prefix + str(i) + '.txt'
        tf_docs[i], idf_docs[i], tf_idf_docs[i] = load_tf_idf(filename)
    return tf_docs, idf_docs, tf_idf_docs


# вывод результатов поиска
def print_results(results, directory):
    for doc, similarity in results:
        filename = directory + '/' + str(doc) + '.html'
        with open(filename, 'r', encoding="utf-8") as f:
            title = f.readline().strip()
            print(title)
            print(filename)
            print('Similarity:', similarity)
            print('-' * 50)


def main():
    inverted_index = load_inverted_index('inverted_index.txt')
    tf_docs, idf_docs, tf_idf_docs = load_all_tf_idf('.', 'tokens/')
    query = "and ноября год"
    args = query.split(' ')
    if len(args) > 1:
        operator = args[0].upper()
    else:
        operator = boolean_search.OR_OPERATOR
    results = boolean_search.search(operator, args[0:])
    args.pop(0)
    if results != 0:
        results = vector_search(args, results, tf_idf_docs)
        print_results(results, 'output')
    else:
        print('0 ответов по вашему запросу')


if __name__ == '__main__':
    main()
