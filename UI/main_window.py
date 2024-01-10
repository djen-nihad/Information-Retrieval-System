import tkinter as tk
from search_engine.evaluations import *
from search_engine.indexations import *
from search_engine.read_write_fils import *
from search_engine.model import *
from UI_Function import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

path_judgements = '../dataset/LISA.REL'
path_query = '../dataset/LISA.QUE'

extraction = None
normalize = None
inverse = False
index = False
queries_from_data = False
path = "../Indexation"
path_dataset = "../dataset"
K = 1.5
B = 0.75
len_dataset = 2
doc = None
value = None
judgments = None

fenetre = tk.Tk()
largeur = fenetre.winfo_screenwidth()
hauteur = fenetre.winfo_screenheight()


def create_spinBox(x, y, min=1, max=1):
    spinbox = tk.Spinbox(fenetre, from_=min, to=max, width=5, textvariable=spinbox_var)
    spinbox.place(x=x, y=y)


def create_checkbar(x, y, list_options):
    checkbox_vars = []  # Liste pour stocker les variables des cases à cocher
    checkboxes = []  # Liste pour stocker les cases à cocher
    x_offset = x
    for option in list_options:
        var = tk.IntVar()
        checkbox = tk.Checkbutton(fenetre, text=option, variable=var)
        checkbox.place(x=x_offset, y=y)
        x_offset += 130  # Espacement vertical entre les cases à cocher
        checkbox_vars.append(var)
        checkboxes.append(checkbox)
    return checkbox_vars

def get_selected_options(checkbox_vars, options):
    selected_options = [options[i] for i, var in enumerate(checkbox_vars) if var.get() == 1]
    return selected_options


def create_radio(x, y, list_options, default="DOCS par TERM"):
    var = tk.StringVar()
    var.set(default)
    x_offset = x
    y_offset = y
    i = 0
    for option in list_options:
        radio_button = tk.Radiobutton(fenetre, text=option, variable=var, value=option)
        if option == "DOCS par TERM":
            radio_button.place(x=350, y=90)
            continue
        elif option == "TERMS par DOCS":
            radio_button.place(x=530, y=90)
            continue
        radio_button.place(x=x_offset, y=y_offset)
        if i == 0: y_offset = y + 100  # Espacement vertical entre les cases à cocher
        if i == 1:
            x_offset += 150
            y_offset = y
            i = 0
            continue
        i += 1

    return var


def create_comboBox(x, y, liste_option):
    variable = tk.StringVar()
    variable.set(liste_option[0])
    combobox = tk.OptionMenu(fenetre, variable, *liste_option)
    combobox.place(x=x, y=y)
    return combobox, variable


def create_label_title(x, y, text):
    label = tk.Label(fenetre, text=text, font=("Helvetica", 12, "bold"))
    label.place(x=x, y=y)


def create_label_title_s(x, y, text):
    label = tk.Label(fenetre, text=text, font=("Helvetica", 9, "bold"))
    label.place(x=x, y=y)


def create_label_text(x, y, text):
    label = tk.Label(fenetre, text=text, font=("Helvetica", 9))
    label.place(x=x, y=y)


def resultat_par_terme(nom_fichier, terme):
    with open(os.path.join(path, nom_fichier), 'r') as f:
        k = 0
        resault = ""
        for line in f:
            if inverse == 1:
                n = line.split()[0]
            else:
                n = line.split()[1]
            if n == terme:
                k = k + 1
                resault = resault + str(k) + "   " + line

        return resault

def find_parameter():
    selected_option_processing = get_selected_options(checkbox_processing, processing_option)
    inverse = matching_radio.get() == "TERMS par DOCS"
    if "Tokenization" in selected_option_processing:
        extraction = 'tokenize'
    else:
        extraction = 'split'
    if "Porter Stemmer" in selected_option_processing:
        Normaliz = 'Porter'
    else:
        Normaliz = 'Lancaster'
    selected_option_index = get_selected_options(checkbox_index, index_option)
    if len(selected_option_index) == 0:
        index = False
    else:
        index = True
    return extraction, Normaliz, inverse, index


def search():
    global inverse, extraction, normalize, index, K, B, queries_from_data, doc, value, judgments

    query = entry.get()
    text_result.delete("1.0", "end")
    selected_queries_dataset = get_selected_options(checkbox_query_Dataset, query_dataset_option)
    if not query and len(selected_queries_dataset) == 0:
        result = "You need to enter a query!"
        text_result.insert("1.0", result)
        return
    if len(selected_queries_dataset) != 0:
        queries_dataset = read_query(path_query)
        judgments = read_judgements(path_judgements)
        k = int(spinbox_var.get()) - 1
        if k < 0:
            text_result.insert("1.0", "Query doesn't exist !")
            return
        query = queries_dataset[k]
        entry.insert(0, query)
        index = False



    result = ""
    extraction, normalize, inverse, index = find_parameter()
    file_name = findFileName(extraction, normalize, inverse, path)
    if index and (matching_radio.get() == "TERMS par DOCS" or matching_radio.get() == "DOCS par TERM"):
        if query.isdigit():
            doc = int(query)
            result = printFile(file_name, doc)
            doc = doc - 1
            if inverse:
                result = format_data_inverse(result)
            else:
                result = format_data(result)
            result = createHeader(inverse) + result
        else:
            result = "ERROR INDEX"
        text_result.insert("1.0", result)
        return
    if matching_radio.get() == "TERMS par DOCS" or matching_radio.get() == "DOCS par TERM":
        terms = processing_Docs(query, extraction, normalize)
        for term in terms:
            result = result + printTerm(file_name, term)
        if result != '' and result != "Document not founded":
            if inverse:
                result = format_data_inverse(result)
            else:
                result = format_data(result)
            result = createHeader(inverse) + result
        else:
            result = "NOT FOUNDED"
        text_result.insert("1.0", result)
    else:
        collections = read_index_file(file_name)
        terms = processing_Docs(query, extraction, normalize)
    if matching_radio.get() == "Vector Space Model":
        if selected_vctoriel_var.get() == "Scalar Product":
            doc, value = scalarProduct(collections, terms)
        elif selected_vctoriel_var.get() == "Cosine Measure":
            doc, value = cosineMeasure(collections, terms)
        else:
            doc, value = jacquardMeasure(collections, terms)
        result = printResultMatching(doc, value)
        result = format_data_matching(result)
        result = createHeader2() + result
        text_result.insert("1.0", result)
    elif matching_radio.get() == "Boolean Model":
        valid = validate_query(query)
        if valid:
            terms = processing_Docs(query, extraction, normalize, False)
            result = evaluate_query(collections, terms)
            result = printResultBool(result)
            result = format_data_matching(result)
            result = createHeader2() + result
            text_result.insert("1.0", result)
        else:
            text_result.insert("1.0", "Query not valid")
        return
    elif matching_radio.get() == "Probabilistic Model (BM25)":
        K = float(entry_k.get())
        B = float(entry_B.get())
        doc, value = modelBM25(collections, terms, K, B)
        result = printResultMatching(doc, value)
        result = format_data_matching(result)
        result = createHeader2() + result
        text_result.insert("1.0", result)
    else:
        print(matching_radio.get())
    if judgments:
        doc_pertinants = judgments[int(spinbox_var.get()) - 1]
        index_doc_selected = np.nonzero(value)
        #doc_selected = doc[index_doc_selected] - 1
        doc_selected = doc[index_doc_selected]
        X, Y = curve_rappel_precision(doc_selected, doc_pertinants, 10)
        courbe = create_matplotlib_graph(X, Y)
        canvas = FigureCanvasTkAgg(courbe, master=fenetre)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=760, y=240)
        pre = precision(doc_selected, doc_pertinants)
        rap = rappel(doc_selected, doc_pertinants)
        fscore = F_Score(doc_selected, doc_pertinants)
        p_5 = P_N(doc_selected, doc_pertinants, 5)
        p_10 = P_N(doc_selected, doc_pertinants, 10)
        print_mesurePerformace(pre, rap, fscore, p_5, p_10)

def print_mesurePerformace(precision,rappel,fscore,p5,p10):
    create_label_title_s(20, 600, "Presision")
    create_label_text(85, 600,str(precision))
    create_label_title_s(160, 600, "P@5")
    create_label_text(225, 600, str(p5))
    create_label_title_s(300, 600, "P@10")
    create_label_text(365, 600, str(p10))
    create_label_title_s(440, 600, "Recall")
    create_label_text(500,600,str(rappel))
    create_label_title_s(580, 600, "F-Score")
    create_label_text(645, 600, str(fscore))

fenetre.geometry(f"{largeur}x{hauteur}")

create_label_title(20, 10, "Query")

# Créer une zone de saisie pour la requête
entry = tk.Entry(fenetre, width=90, relief="solid", borderwidth=0.5)
entry.place(x=90, y=15)

# Créez un bouton "Valider"
bouton = tk.Button(fenetre, text="search", command=search)
bouton.place(x=680, y=13)

create_label_title_s(30, 60, "Processing")

create_label_text(820,13,"Queries Dataset")
query_dataset_option = [""]
checkbox_query_Dataset = create_checkbar(790, 13, query_dataset_option)

spinbox_var = tk.StringVar()
spinBox = create_spinBox(x=940, y=13, min=1, max=len_dataset)
spinbox_var.set(1)

processing_option = ["Tokenization", "Porter Stemmer"]
x, y = 10, 90
checkbox_processing = create_checkbar(x, y, processing_option)

create_label_title_s(290, 60, "Index")
index_option = [" "]
x = 300

checkbox_index = create_checkbar(x, y, index_option)



create_label_title(20, 140, "Result")

text_result = tk.Text(fenetre, width=90, height=25, bd=0.5, relief="solid")
text_result.place(x=20, y=190)

x = 800
y = 90
create_label_title_s(790, 60, "Matching")
matching_option_radio = ["DOCS par TERM", "TERMS par DOCS", "Vector Space Model",
                         "Boolean Model", "Probabilistic Model (BM25)", "Data Mining Model"]
matching_radio = create_radio(x, y, matching_option_radio)

create_label_text(980,120,'K')
# Créer une zone de saisie pour la requête
entry_k = tk.Entry(fenetre, width=10, relief="solid", borderwidth=0.5)
entry_k.insert(0,str(K))
entry_k.place(x=1000, y=120)

create_label_text(980,150,'B')
entry_B = tk.Entry(fenetre, width=10, relief="solid", borderwidth=0.5)
entry_B.insert(0, str(B))
entry_B.place(x=1000, y=150)


y = 125
vectoriel_option_checkbar = ["Scalar Product", "Cosine Measure", "Jaccard Measure"]
vectoriel_comboBox, selected_vctoriel_var = create_comboBox(x, y, vectoriel_option_checkbar)

# Lancer la boucle principale de l'application
fenetre.mainloop()
