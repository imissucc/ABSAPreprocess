import re


def placeholder_constructor(term_size, polarity, join=False):

    POL = {
        "positive": "POS",
        "neutral": "NEU",
        "negative": "NEG"
    }
    BA = "$B$"
    IA = "$I$"

    if join:
        P = POL[polarity]  # "POS"
        ph = "$B{}$".format(P)
        iph = "$I{}$".format(P)
        if term_size > 1:
            for _ in range(term_size - 1):
                ph += " {}".format(iph)  # "$B-POS$ $I-POS$"
    else:
        ph = BA
        if term_size > 1:
            for _ in range(term_size - 1):
                ph += " {}".format(IA) # "$B$ $I$"

    return ph

def replace_with_index(text, placeholders, positions):

    new_text = []
    last_end = 0
    for i in range(len(positions)):
        pos = positions[i]
        ph = placeholders[i]
        new_text.append(text[last_end:pos[0]])
        new_text.append(ph)
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
    labels = ("$BPOS$","$BNEU$", "$BNEG$",
              "$IPOS$","$INEU$", "$INEG$",
              "$B$", "$I$")
    words = text.split(" ")
    text_label = []
    for w in words:
        if w not in labels:
            text_label.append("O")
        else:
            text_label.append(w[1:-1])

    return " ".join(text_label)

def placeholder_text_reverse(text_with_ph, aspect_terms):

    text = text_with_ph
    for term in aspect_terms:
        t_size = len(term.split())
        t_ph = "$B$"
        if len(term.split()) > 1:
            for _ in range(t_size - 1):
                t_ph += " $I$"
            text = text.replace(t_ph, term, 1)
        else:
            text = text.replace(t_ph, term, 1)

    return text