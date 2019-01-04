# [text, term label, term]
from SemEval14 import SemEval14XMLReader
import re


def AspectTermPlaceHolder(count):

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


def AspectTermReplacement(text, aspect_terms):

    # text: str
    # aspect_terms: [(aspect_term, polarity, (from, to))...]
    ph_terms = []
    ap_terms = []
    pos = []
    for t in aspect_terms:
        # t: (aspect_term, polarity, (from, to))
        aspect_term = t[0]
        aspect_count = len(aspect_term.split())
        ph = AspectTermPlaceHolder(count=aspect_count) # "$BA$ $IA$"
        ph_terms.append(ph)
        ap_terms.append(aspect_term)
        pos.append(t[2])

    # phs: [(aspect_place_holder, (from, to))...]
    new_text = replace_with_index(text, ph_terms, pos)
    new_text = washer(new_text)
    ap_terms = ", ".join(ap_terms)

    return new_text, ap_terms


def LabelConstructor(text):

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


def SE14_ATEDataPrepare(file):

    datas, _ = SemEval14XMLReader(file=file)
    # datas: [data/.id/.text/.aspect_terms/.aspect_categories]
    outputs = []
    for data in datas:
        text = data.text
        aspect_terms = data.aspect_terms

        if aspect_terms is not None:
            # "All the $BA$ and $BA$ were fabulous, the $BA$ was mouth watering and the $BA$ was delicious!!!"
            new_text, ap_terms = AspectTermReplacement(text, aspect_terms)
            text_label = LabelConstructor(new_text)

        else:
            # don't have aspect terms
            new_text = washer(text)
            text_label = LabelConstructor(new_text)
            ap_terms = None

        outputs.append([new_text, text_label, ap_terms])

    return outputs


if __name__ == "__main__":

    datas = SE14_ATEDataPrepare(file="data/restaurants-trial.xml")
    for data in datas:
        print(data)