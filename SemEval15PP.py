# [text, term label, term, category]

import csv
import codecs

from utils import *
from SemEval15 import SemEval15XMLReader


def aspect_term_replacement(text, opinions):

    # text: str
    # opinions: [(term, entity#attribute, polarity, (from, to))...]
    ph_terms = [] # place holder terms
    ap_terms = [] # aspect terms
    categories = [] # categories
    pos = []
    for t in opinions:
        # t: (term, entity#attribute, polarity, (from, to))
        aspect_term = t[0] # maybe == "NULL"
        if aspect_term != "NULL":
            aspect_count = len(aspect_term.split())
            ph = aspect_term_placeholder(count=aspect_count) # "$BA$ $IA$"
            ph_terms.append(ph)
            ap_terms.append(aspect_term)
            pos.append(t[3])

        categories.append(t[1])

    # if aspect_terms is not None
    assert len(ph_terms) == len(ap_terms)
    if len(ph_terms) > 0:
        new_text = replace_with_index(text, ph_terms, pos)
        ap_terms = ",".join(ap_terms)
    else:
        new_text = text
        ap_terms = None
    categories = ",".join(set(categories))

    return new_text, ap_terms, categories

def SE15_ATEDataPrepare(file, rm_none_aspect):

    datas, _ = SemEval15XMLReader(file=file)
    # datas: [data/.id/.sentences:
    #                   [sentence/.id/.text/.opinions]
    #        ]
    outputs = []

    for data in datas:
        for sentence in data.sentences:
            text = sentence.text
            opinions = sentence.opinions # [(term, entity#attribute, polarity, (from, to))]

            # opinion is always exist
            # "All the $BA$ and $BA$ were fabulous, the $BA$ was mouth watering and the $BA$ was delicious!!!"
            new_text, ap_terms, ap_categories = aspect_term_replacement(text, opinions)
            new_text = washer(new_text)
            text_label = label_constructor(new_text)

            # if ignore sentences without aspect
            if rm_none_aspect and ap_terms is None:
                continue
            outputs.append([new_text, text_label, ap_terms, ap_categories])

    return outputs


if __name__ == "__main__":

    name = "absa-2015_restaurants_trial"
    datas = SE15_ATEDataPrepare(file="data/{}.xml".format(name),
                                rm_none_aspect=True)

    # write to csv file
    with codecs.open("data/{}.csv".format(name), "w", "utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(datas)