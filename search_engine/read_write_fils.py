import os
import numpy as np


def read_query(path):
    queries = []
    with open(path, 'r') as f:
        all_query = f.read()
        all_query = all_query.split('#\n')
        for query in all_query:
            query = query.split()
            if len(query) > 1:
                query.pop(0)
                query = " ".join(query)
                queries.append(query)
    return queries


def read_judgements(path):
    judgements = []
    with open(path, 'r') as f:
        all_judgements = f.read()
        all_judgements = all_judgements.split('\n\n')
        for judgement in all_judgements:
            judgement = judgement.split('\n')
            judgement.pop(0)
            judgement.pop(0)
            judgement = " ".join(judgement)
            judgement = judgement.split(" ")
            judgement.pop(-1)
            for i in range(len(judgement)):
                judgement[i] = int(judgement[i]) - 1
            judgements.append(judgement)
    return judgements


def read_LISA_dataset(path):
    docs = []
    queries = []
    judgements = []
    for file in os.listdir(path):
        path_file = os.path.join(path, file)
        if file == 'LISA.QUE':
            queries = read_query(path_file)
            continue
        elif file == 'LISA.REL':
            judgements = read_judgements(path_file)
            continue
        elif file == 'README':
            continue
        with open(path_file, 'r') as f:
            documents_bruit = f.read()
            documents_bruit = documents_bruit.split("********************************************")
            documents_bruit.pop(-1)
            for doc_bruit in documents_bruit:
                doc = doc_bruit.split('\n')
                if doc[0] == '\n' or doc[0] == '': doc.pop(0)
                doc.pop(0)
                doc = "\n".join(doc)
                docs.append(doc)
    return docs, queries, judgements


def create_descriptor_file(file_name, collection):
    with open(file_name, "w") as f:
        for i in range(len(collection)):
            doc, freq, weights = collection[i]
            for j in range(len(doc)):
                f.write(str(i + 1) + " " + doc[j] + " " + str(freq[j]) + " " + str(weights[j]) + "\n")


def create_inverse_file(file_name, collection):
    all_term = []
    for i in range(len(collection)):
        doc, freq, weights = collection[i]
        for j in range(len(doc)):
            all_term.append(doc[j] + " " + str(i + 1) + " " + str(freq[j]) + " " + str(weights[j]))
    all_term = sorted(all_term)
    with open(file_name, "w") as f:
        f.write('\n'.join(all_term))


def read_index_file(path):
    with open(path, 'r') as file:
        i = 0
        terms, frequencies, weights = [], [], []
        collection = []
        for line in file:
            columns = line.split()
            if int(columns[0]) != i:
                i += 1
                if i != 1:
                    collection.append([np.array(terms), np.array(frequencies), np.array(weights)])
                terms, frequencies, weights = [], [], []
            terms.append(columns[1])
            frequencies.append(int(columns[2]))
            weights.append(float(columns[3]))
        collection.append([np.array(terms), np.array(frequencies), np.array(weights)])
        return collection

# def read_index_file(path):
#     with open(path, 'r') as file:
#         i = 1
#         terms, frequencies, weights = [], [], []
#         collection = []
#         for line in file:
#             columns = line.split()
#             if int(columns[0]) != i:
#                 i += 1
#                 if i != 1:
#                     collection.append([np.array(terms), np.array(frequencies), np.array(weights)])
#                 terms, frequencies, weights = [], [], []
#             terms.append(columns[1])
#             frequencies.append(int(columns[2]))
#             weights.append(float(columns[3]))
#         collection.append([np.array(terms), np.array(frequencies), np.array(weights)])
#         return collection