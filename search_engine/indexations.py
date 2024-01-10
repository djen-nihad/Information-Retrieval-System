import nltk
from search_engine.read_write_fils import *


def processing_Docs(doc, extraction='tokenize', Normalize='Porter', stopWords=True):
    # terms extractions
    if extraction == 'tokenize':
        regExp = nltk.RegexpTokenizer('(?:[A-Za-z]\.)+|[A-Za-z]+[\-@]\d+(?:\.\d+)?|\d+[A-Za-z]+|\d+(?:[\.\,]\d+)?%?|\w+(?:[\-/]\w+)*')
        doc_ = regExp.tokenize(doc)
    elif extraction == 'split':
        doc_ = doc.split()
    else:
        print('Terms extraction method not recognized')
        doc_ = doc
    if stopWords:
        stopWordsList = nltk.corpus.stopwords.words('english')
        doc_ = [word for word in doc_ if word.lower() not in stopWordsList]
    if Normalize == 'Porter':
        Porter = nltk.PorterStemmer()
        doc_ = [Porter.stem(word) for word in doc_]
    elif Normalize == 'Lancaster':
        Lancaster = nltk.LancasterStemmer()
        doc_ = [Lancaster.stem(word) for word in doc_]
    else:
        print('Normalization method not recognized')
    return doc_


def frequencyDocs(collection):
    collection = [list(np.unique(doc, return_counts=True)) for doc in collection]
    return collection


def calculateWeights(freq, maximum, N, n):
    result = (freq / maximum) * np.log10(N / n + 1)
    return round(result, 4)


def calculateNbrOccurrenceInDocs(term, collection):
    cpt = 0
    for doc in collection:
        exist = np.isin(term, doc)
        if np.any(exist): cpt += 1
    return cpt


def calculateWeightsDocs(collection):
    N = len(collection)
    for i, (terms, frequencies) in enumerate(collection):
        max_freq = np.max(frequencies)
        weights = [
            calculateWeights(freq, max_freq, N, calculateNbrOccurrenceInDocs(term, collection))
            for term, freq in zip(terms, frequencies)
        ]
        collection[i].append(weights)
    return collection


def indexation_LISA_dataset(path):
    docs, queries, judgments = read_LISA_dataset(path)

    docs_split_Porter = [processing_Docs(doc, extraction='split', Normalize='Porter', stopWords=True) for doc in docs]
    docs_split_Porter = frequencyDocs(docs_split_Porter)
    collection_split_Porter = calculateWeightsDocs(docs_split_Porter)
    descriptorSplitPorter_path = "Indexation/DescriptorSplitPorter.txt"
    create_descriptor_file(descriptorSplitPorter_path, collection_split_Porter)



    #
    #
    #
    # docs_split_Lancaster = [processing_Docs(doc, extraction='split', Normalize='Lancaster', stopWords=True) for doc in
    #                         docs]
    # docs_tokenize_Porter = [processing_Docs(doc, extraction='tokenize', Normalize='Porter', stopWords=True) for doc in
    #                         docs]
    # docs_tokenize_Lancaster = [processing_Docs(doc, extraction='tokenize', Normalize='Lancaster', stopWords=True) for doc
    #                            in docs]
    #
    # docs_split_Lancaster = frequencyDocs(docs_split_Lancaster)
    # docs_tokenize_Porter = frequencyDocs(docs_tokenize_Porter)
    # docs_tokenize_Lancaster = frequencyDocs(docs_tokenize_Lancaster)
    #
    # collection_split_Lancaster = calculateWeightsDocs(docs_split_Lancaster)
    # collection_tokenize_Porter = calculateWeightsDocs(docs_tokenize_Porter)
    # collection_tokenize_Lancaster = calculateWeightsDocs(docs_tokenize_Lancaster)
    #
    # descriptorSplitLancaster_path = "Indexation/DescriptorSplitLancaster.txt"
    # descriptorTokenizePorter_path = "Indexation/DescriptorTokenizePorter.txt"
    # descriptorTokenizeLancaster_path = "Indexation/DescriptorTokenizeLancaster.txt"
    # inverseSplitLancaster_path = "Indexation/InverseSplitLancaster.txt"
    # inverseSplitPorter_path = "Indexation/InverseSplitPorter.txt"
    # inverseTokenizePorter_path = "Indexation/InverseTokenizePorter.txt"
    # inverseTokenizeLancaster_path = "Indexation/InverseTokenizeLancaster.txt"
    #
    # create_descriptor_file(descriptorSplitLancaster_path, collection_split_Lancaster)
    # create_descriptor_file(descriptorTokenizePorter_path, collection_tokenize_Porter)
    # create_descriptor_file(descriptorTokenizeLancaster_path, collection_tokenize_Lancaster)
    #
    # create_inverse_file(inverseSplitPorter_path, collection_split_Porter)
    # create_inverse_file(inverseSplitLancaster_path, collection_split_Lancaster)
    # create_inverse_file(inverseTokenizePorter_path, collection_tokenize_Porter)
    # create_inverse_file(inverseTokenizeLancaster_path, collection_tokenize_Lancaster)
