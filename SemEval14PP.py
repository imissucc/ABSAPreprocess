# [text, term label, term, category]

import csv
import codecs

from utils import *
from SemEval14 import SemEval14XMLReader


def aspect_term_replacement(text, aspect_terms):

    # text: str
    # aspect_terms: [(aspect_term, (from, to))...]
    ph_terms = []
    ap_terms = []
    pos = []
    for t in aspect_terms:
        # t: (aspect_term, (from, to))
        aspect_term = t[0]
        aspect_count = len(aspect_term.split())
        ph = aspect_term_placeholder(count=aspect_count) # "$BA$ $IA$"
        ph_terms.append(ph)
        ap_terms.append(aspect_term)
        pos.append(t[1])

    # phs: [(aspect_place_holder, (from, to))...]
    assert len(ph_terms) == len(ap_terms)
    new_text = replace_with_index(text, ph_terms, pos)
    ap_terms = ",".join(ap_terms)

    return new_text, ap_terms


def aspect_category_constructor(aspect_categories):

    # aspect_categories: [category]
    output = aspect_categories[0]
    category_size = len(aspect_categories)
    if category_size > 1:
        for i in range(1, category_size):
            output += ",{}".format(aspect_categories[i][0])

    return output


def SE14_ATEDataPrepare(file, rm_none_aspect=False):

    datas, _ = SemEval14XMLReader(file=file)
    # datas: [data/.id/.text/.aspect_terms/.aspect_categories]
    outputs = []
    for data in datas:
        text = data.text
        aspect_terms = data.aspect_terms
        aspect_categories = data.aspect_categories

        if aspect_terms is not None:
            # "All the $BA$ and $BA$ were fabulous, the $BA$ was mouth watering and the $BA$ was delicious!!!"
            new_text, ap_terms = aspect_term_replacement(text, aspect_terms)
            new_text = washer(new_text)
            text_label = label_constructor(new_text)
            ap_categories = aspect_category_constructor(aspect_categories) if aspect_categories is not None else None
            outputs.append([new_text, text_label, ap_terms, ap_categories])

        else:
            if rm_none_aspect:
                continue
            else:
                # don't have aspect terms
                new_text = washer(text)
                text_label = label_constructor(new_text)
                ap_terms = None
                ap_categories = None
                outputs.append([new_text, text_label, ap_terms, ap_categories])

    return outputs


if __name__ == "__main__":

    file_name = {
        "14restaurant_train": "datasets/SemEval2014/Restaurants_Train_v2.xml",
        "14restaurant_test": "datasets/SemEval2014/ABSA_TestData_PhaseB/Restaurants_Test_Data_phaseB.xml",
        "14laptop_train": "datasets/SemEval2014/Laptop_Train_v2.xml",
        "14laptop_test": "datasets/SemEval2014/ABSA_TestData_PhaseB/Laptops_Test_Data_phaseB.xml"
    }

    for k, v in file_name.items():

        datas = SE14_ATEDataPrepare(file=v,
                                    rm_none_aspect=False)
        print(len(datas))
        # write to csv file
        with codecs.open("resources/AspectTermExtraction/{}.csv".format(k), "w", "utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(datas)