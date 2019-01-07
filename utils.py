import re

def aspect_term_placeholder(count):

    BA = "$BA$"
    IA = "$IA$"
    place_holder = BA
    if count > 1:
        for _ in range(count-1):
            place_holder += " {}".format(IA)

    return place_holder


def replace_with_index(text, terms, positions):

    new_text = []
    last_end = 0
    for i in range(len(positions)):
        pos = positions[i]
        term = terms[i]
        new_text.append(text[last_end:pos[0]])
        new_text.append(term)
        last_end = pos[1]
    new_text.append(text[last_end:])

    return "".join(new_text)


def washer(string):

    # remove digits
    string = re.sub(r'\d+', " ", string)
    # retain only alphabets and digits
    string = re.sub(r"[^A-Za-z$\']", " ", string)
    # dollar
    string = re.sub(r"\s\$\s", " ", string)
    string = re.sub(r"\s\$$", "", string)
    string = re.sub(r"^\$\s", "", string)
    # multi space
    string = re.sub(r"\s{2,}", " ", string)
    # remove space from start and end
    string = re.sub(r"\s$", "", string)
    string = re.sub(r"^\s", "", string)

    return string.strip()

def label_constructor(text):

    # text: text with aspect term place holder
    labels = ("$BA$", "$IA$", "$BO$", "$IA$")
    words = text.split(" ")
    text_label = []
    for w in words:
        if w not in labels:
            text_label.append("N")
        else:
            text_label.append(w[1:3])

    return " ".join(text_label)