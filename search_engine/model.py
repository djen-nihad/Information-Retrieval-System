import numpy as np


def scalarProduct(collection, query_normalise):
    # document = [ [Terms] , [Frequency ] , [weight]
    scalarProductValue = []
    for document in collection:
        w = document[2]
        v = np.zeros(document[0].shape)
        index_ = np.where(np.isin(document[0], query_normalise))
        v[index_] = 1
        val = np.sum(w * v)
        scalarProductValue.append(round(val, 4))
    index = np.argsort(scalarProductValue)[::-1]
    docs = index + 1
    scalarProductValue = np.array(scalarProductValue)
    return docs, scalarProductValue[index]


def cosineMeasure(collection, query_normalise):
    # document = [ [Terms] , [Frequency ] , [weight]
    cousin_measure_value = []
    for document in collection:
        w = document[2]
        v = np.zeros(document[0].shape)
        index_ = np.where(np.isin(np.array(document[0]), np.array(query_normalise)))
        v[index_] = 1
        a = (np.sqrt(np.sum(v ** 2))) * (np.sqrt(np.sum(w ** 2)))
        if a == 0:
            val = 0
        else:
            val = np.sum(w * v) / a
        cousin_measure_value.append(round(val, 4))
    index = np.argsort(cousin_measure_value)[::-1]
    docs = index + 1
    cousin_measure_value = np.array(cousin_measure_value)
    return docs, cousin_measure_value[index]


def jacquardMeasure(collection, query_normalise):
    # document = [ [Terms] , [Frequency ] , [weight]
    jacquardMeasureValue = []
    for document in collection:
        w = document[2]
        v = np.zeros(document[0].shape)
        index_ = np.where(np.isin(document[0], query_normalise))
        v[index_] = 1
        val = np.sum(w * v) / (np.sum(v ** 2) + np.sum(w ** 2) - np.sum(v * w))
        jacquardMeasureValue.append(round(val, 4))
    jacquardMeasureValue = np.array(jacquardMeasureValue)
    index = np.argsort(jacquardMeasureValue)[::-1]
    docs = index + 1
    return docs, jacquardMeasureValue[index]


def modelBM25(collection, query_normalise, K, B):
    N = len(collection)
    n = np.zeros(len(query_normalise))
    avdl = 0

    # Calculate average document length (avdl)
    for doc in collection:
        avdl += np.sum(doc[1])

    avdl = avdl / len(collection)

    BM25Values = []

    # Calculate n for each query term
    for i in range(len(query_normalise)):
        for doc in collection:
            index = np.where(doc[0] == query_normalise[i])
            if len(index[0]) != 0:
                n[i] = n[i] + 1

    # Calculate BM25 score for each document
    for document in collection:
        RSV = 0
        dl = np.sum(document[1])
        for i in range(len(query_normalise)):
            index = np.where(document[0] == query_normalise[i])
            if len(index[0]) == 0:
                continue
            frequency = document[1][index][0]
            RSV = RSV + (frequency / (K * ((1 - B) + (B * (dl / avdl))) + frequency)) * \
                  np.log10((N - n[i] + 0.5) / (n[i] + 0.5))

        # Append the BM25 score to the list
        BM25Values.append(round(RSV, 4))

    BM25Values = np.array(BM25Values)

    # Sort documents by BM25 score in descending order
    index = np.argsort(BM25Values)[::-1]
    docs = index + 1

    return docs, BM25Values[index]


def type_(term):
    if term.upper() == 'AND':
        return 'AND'
    elif term.upper() == 'OR':
        return 'OR'
    elif term.upper() == 'NOT':
        return 'NOT'
    else:
        return 'term'


def validate_query(query):
    query = query.split()
    x = []
    for i in range(len(query)):
        if type_(query[i]) == 'term':
            if len(x) != 0 and (x[-1] != "OPERATEUR" and x[-1] != "NOT"): return False
            x.append(query[i])
        elif type_(query[i]) == 'AND':
            if len(x) == 0 or i + 1 >= len(query) or type_(query[i + 1]) == 'OR':
                return False
            else:
                x.clear()
                x.append("OPERATEUR")
        elif type_(query[i]) == 'OR':
            if len(x) == 0 or i + 1 >= len(query) or type_(query[i + 1]) == 'AND':
                return False
            else:
                x.clear()
                x.append("OPERATEUR")
        else:
            if len(x) != 0:
                if x[-1] != "OPERATEUR": return False
            if i + 1 >= len(query) or type_(query[i + 1]) != 'term':
                return False
            else:
                x.clear()
                x.append('NOT')

    return True


def evaluate_query(collections, query):
    result = []
    k = 0
    for doc in collections:
        k = k + 1
        query_copy = ""
        for i in range(len(query)):
            if type_(query[i]) == 'term':
                if np.any(np.isin(query[i], doc[0])):
                    query_copy = query_copy + "1 "
                else:
                    query_copy = query_copy + "0 "
            else:
                query_copy = query_copy + query[i] + " "

        if eval(query_copy) == 1:  result.append(k)

    return result
