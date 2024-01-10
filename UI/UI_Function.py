import os
from matplotlib.figure import Figure


def format_data(data):
    lines = data.split('\n')
    formatted_data = ""
    for line in lines:
        columns = line.split()
        if columns:
            formatted_line = f"{columns[0]:<4}{columns[1]:<7}{columns[2]:<25}{columns[3]:<7}{columns[4]:<7}\n"
            formatted_data += formatted_line
    return formatted_data


def format_data_inverse(data):
    lines = data.split('\n')
    formatted_data = ""
    for line in lines:
        columns = line.split()
        if columns:
            formatted_line = f"{columns[0]:<4}{columns[1]:<25}{columns[2]:<7}{columns[3]:<7}{columns[4]:<7}\n"
            formatted_data += formatted_line
    return formatted_data


def format_data_matching(data):
    lines = data.split('\n')
    formatted_data = ""
    for line in lines:
        columns = line.split()
        if columns:
            formatted_line = f"{columns[0]:<7}{columns[1]:<25}\n"
            formatted_data += formatted_line
    return formatted_data


def createHeader(inverse):
    if inverse:
        header = "N° Term  N°Doc  Freq  Weight "
        header = format_data_inverse(header)
    else:
        header = "N°  N°Doc Term  Freq  Weight "
        header = format_data(header)
    return header


def createHeader2():
    header = "N°doc  Relevance"
    header = format_data_matching(header)
    return header


def findFileName(extraction, Normalize, inverse, path):
    if inverse:
        file_name = "Inverse"
    else:
        file_name = "Descriptor"

    if extraction == 'tokenize':
        file_name = file_name + "Tokenize"
    else:
        file_name = file_name + "Split"
    if Normalize == 'Porter':
        file_name = file_name + "Porter"
    else:
        file_name = file_name + "Lancaster"
    file_name = file_name + ".txt"
    return os.path.join(path, file_name)


def printFile(path, nbrDoc):
    if 'Inverse' in path:
        inverse = True
    else:
        inverse = False
    with open(path, 'r') as f:
        k = 0
        result = ""
        for line in f:
            if inverse:
                n = line.split()[1]
            else:
                n = line.split()[0]
            n = int(n)
            if not inverse and n > nbrDoc:
                break
            elif n == nbrDoc:
                k = k + 1
                result = result + str(k) + "   " + line
        if result == "":
            result = "Document not founded"
        return result


def printTerm(path, term):
    if 'Inverse' in path:
        inverse = True
    else:
        inverse = False
    with open(path, 'r') as f:
        k = 0
        result = ""
        for line in f:
            if inverse:
                n = line.split()[0]
            else:
                n = line.split()[1]
            if n == term:
                k = k + 1
                result = result + str(k) + "   " + line
        return result


def printResultBool(doc):
    result = ""
    for i_doc in doc:
        result = result + str(i_doc) + " " + 'Yes' + '\n'
    return result


def printResultMatching(doc, value):
    result = ""
    for i in range(len(doc)):
        if value[i] == 0: continue
        result = result + str(doc[i] + 1) + "  " + str(value[i]) + '\n'
    return result


def create_matplotlib_graph(X, Y):
    color_plot = "#953735"
    color_points = "#F2DCDB"
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(X, Y, color=color_plot)
    ax.grid()
    scatter_points = ax.scatter(X, Y, color=color_points, zorder=2)
    scatter_points.set_edgecolor(color_plot)
    fig.patch.set_edgecolor('black')
    fig.patch.set_linewidth(1)
    ax.set_xlabel('Rappel')
    ax.set_ylabel('Précision')
    ax.set_title("Curve Recall/Precision")

    # Set top and right spines' color to background color
    ax.spines['top'].set_color(ax.get_facecolor())
    ax.spines['right'].set_color(ax.get_facecolor())

    return fig
