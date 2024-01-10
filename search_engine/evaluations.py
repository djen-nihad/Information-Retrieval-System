
def precision(doc_selected, doc_pertinent):
    count = 0
    doc_selected = doc_selected.tolist()
    doc_pertinent = doc_pertinent
    for doc in doc_selected:
        if doc in doc_pertinent: count = count + 1
    return round(count / len(doc_selected), 4)


def P_N(doc_selected, doc_pertinent, N):
    if N == 0: return 0
    doc_N = doc_selected[:N + 1].tolist()
    count = 0
    for doc in doc_N:
        if doc in doc_pertinent:
            count = count + 1
    return round(count / N, 4)


def rappel(doc_selected, doc_pertinent):
    count = 0
    doc_selected = doc_selected.tolist()
    doc_pertinent = doc_pertinent
    for doc in doc_selected:
        if doc in doc_pertinent: count = count + 1
    return round(count / len(doc_pertinent), 4)


def F_Score(doc_selected, doc_pertinent):
    try:
        R = rappel(doc_selected, doc_pertinent)
        P = precision(doc_selected, doc_pertinent)
        return round((2 * P * R) / (P + R), 4)
    except:
        return 0


def curve_rappel_precision(doc_selected, doc_pertinents, max_classifications):
    precisions = []
    rappels = []
    for i in range(max_classifications):
        doc_selected_i = doc_selected[:i + 1]
        precisions.append(precision(doc_selected_i, doc_pertinents))
        rappels.append(rappel(doc_selected_i, doc_pertinents))
    X = []
    Y = []
    threshold = 0
    for i in range(max_classifications + 1):
        X.append(threshold)
        max_precision = 0
        for j in range(max_classifications):
            if rappels[j] >= threshold and precisions[j] > max_precision:
                max_precision = precisions[j]
        Y.append(round(max_precision, 2))
        threshold = round(threshold + 0.1, 1)

    return X, Y
