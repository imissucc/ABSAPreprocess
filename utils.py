import re
import csv
import codecs


def polarity_addition(pol1, pol2):
    # neutral + * = *
    # * + * = *
    # *1 + *2 = conflict

    if pol1 == "neutral":
        return pol2
    else:
        if pol2 == "neutral" or pol2 == pol1:
            return pol1
        elif pol2 != pol1:
            return "conflict"


def placeholder_constructor(term_size, polarity, join=False):

    POL = {
        "positive": "POS",
        "neutral": "NEU",
        "negative": "NEG",
        "conflict": "CON"
    }
    BA = "$B$"
    IA = "$I$"

    if join:
        P = POL[polarity]  # "POS"
        ph = "$B-{}$".format(P)
        iph = "$I-{}$".format(P)
        if term_size > 1:
            for _ in range(term_size - 1):
                ph += " {}".format(iph)  # "$B-POS$ $I-POS$"
    else:
        ph = BA
        if term_size > 1:
            for _ in range(term_size - 1):
                ph += " {}".format(IA) # "$B$ $I$"

    return ph

def replace_with_index(text, aspect_map):

    # text: str
    # aspect_map: dict[position] = (aspect_term, placeholder)

    text_ph = []
    last_end = 0
    # positions should sort
    for pos, (_, ph) in aspect_map.items():
        text_ph.append(text[last_end:pos[0]])
        text_ph.append(ph)
        last_end = pos[1]
    text_ph.append(text[last_end:])
    text_ph = "".join(text_ph)

    return text_ph


def washer(string):

    # remove digits
    string = re.sub(r'\d+', " ", string)
    # retain only alphabets and digits
    string = re.sub(r"[^A-Za-z$\'-]", " ", string)
    # punctuation
    string = re.sub(r"\'\$", "\' $", string) # seperate ' and $
    string = re.sub(r"\$\'", "$ \'", string) # seperate $ and '
    string = re.sub(r"-\$", "- $", string)  # seperate - and $
    string = re.sub(r"\$-", "$ -", string)  # seperate $ and -
    string = re.sub(r"\$\$", "$ $", string) # seperate $ and $
    string = re.sub(r"\s\'\s", " ", string) # remove single '
    string = re.sub(r"\s\'\s", " ", string) # same as the last line
    string = re.sub(r"\s\$\s", " ", string) # remove single $
    string = re.sub(r"\s\$\s", " ", string) # same as the last line
    string = re.sub(r"\s-\s", " ", string)  # remove single -
    string = re.sub(r"\s-\s", " ", string)  # same as the last line
    string = re.sub(r"\s\$$", "", string) # single $ at the end of sentence
    string = re.sub(r"^\$\s", "", string) # single $ at the begin of sentence
    # multi space
    string = re.sub(r"\s{2,}", " ", string)
    # remove space from start and end
    string = re.sub(r"\s$", "", string)
    string = re.sub(r"^\s", "", string)

    return string.strip()

def label_constructor(text):

    # text: text with aspect term place holder
    labels = ("$B-POS$","$B-NEU$", "$B-NEG$", "$B-CON$",
              "$I-POS$","$I-NEU$", "$I-NEG$", "$I-CON$",
              "$B$", "$I$")
    words = text.split(" ")
    text_label = []
    for w in words:
        if w not in labels:
            text_label.append("O")
        else:
            text_label.append(w[1:-1])

    return " ".join(text_label)

def verifier(datas):

    verified = []
    failed_count = 0

    for i in range(len(datas)):
        text = datas[i][0].split()
        label = datas[i][1].split()
        if len(text) != len(label):
            print("[WARN] DROPED DATA: {}".format(datas[i]))
            failed_count += 1
        else:
            verified.append(datas[i])

    return verified, failed_count


def placeholder_reverse(text_ph, aspect_map):

    # text_ph: str
    # aspect_map: dict[position] = (aspect_term, placeholder)

    ph_list = ["$B-POS$", "$B-NEU$", "$B-NEG$", "$B-CON$",
               "$I-POS$", "$I-NEU$", "$I-NEG$", "$I-CON$",
               "$B$", "$I$"]
    terms = list(aspect_map.values()) # list[(aspect_term, placeholder)]
    text_ph = text_ph.split()
    term_size = len(terms)

    term_id = 0
    t_id = 0
    for i in range(len(text_ph)):
        w = text_ph[i] # word in text_ph
        t = terms[term_id][0].split()
        t_size = len(t)
        if w not in ph_list:
            continue
        # w in ph_list
        text_ph[i] = t[t_id] # replacement
        if t_id < t_size-1:
            t_id += 1
        else:
            t_id = 0 # reset
            if term_id < term_size-1:
                term_id += 1
            else:
                break

    return " ".join(text_ph)