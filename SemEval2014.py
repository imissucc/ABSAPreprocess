import xml.sax
import csv
import codecs

from utils import *


class SemEval14Data:

    def __init__(self):
        self._id = None
        self._text = None
        self._aspect_categories = None
        self._aspect_terms = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        assert isinstance(value, str)
        self._id = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def aspect_terms(self):
        return self._aspect_terms

    @aspect_terms.setter
    def aspect_terms(self, value):
        self._aspect_terms = value

    @property
    def aspect_categories(self):
        return self._aspect_categories

    @aspect_categories.setter
    def aspect_categories(self, value):
        self._aspect_categories = value

# SemEval Aspect Term Extraction
class SemEval14Handler(xml.sax.ContentHandler):

    def __init__(self):

        super(SemEval14Handler, self).__init__()
        self.CurrentTag = None
        self.id = None
        self.text = None
        self.aspect_terms = None
        self.aspect_categories = None
        self.datas = []

    def startElement(self, tag, attributes):

        self.CurrentTag = tag
        if tag == "aspectTerms":
            # reset
            self.aspect_terms = []
        elif tag == "aspectCategories":
            # reset
            self.aspect_categories = []
        elif tag == "sentence":
            # reset data instance
            self.data = SemEval14Data()
            self.id = attributes["id"]
        elif tag == "aspectTerm":
            # term data
            term = attributes["term"]
            fromto = (int(attributes["from"]), int(attributes["to"]))
            polarity = attributes["polarity"]
            if polarity != "conflict": # remove conflict aspect from corpus
                self.aspect_terms.append((term, fromto, polarity))
        elif tag == "aspectCategory":
            # category data
            category = attributes["category"]
            self.aspect_categories.append(category)

    def characters(self, content):

        if self.CurrentTag == "text":
            self.text = content

    def endElement(self, tag):

        if tag == "sentence":
            self.data.id = self.id
            self.datas.append(self.data)
        elif tag == "text":
            self.data.text = self.text
        elif tag == "aspectTerms":
            if self.aspect_terms is None or len(self.aspect_terms) != 0:
                self.data.aspect_terms = self.aspect_terms
            else: # is not None and len=0
                self.data.aspect_terms = None
        elif tag == "aspectCategories":
            self.data.aspect_categories = self.aspect_categories


def SemEval14XMLReader(file):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = SemEval14Handler()
    parser.setContentHandler(Handler)

    parser.parse(file)

    desc = ">>> datafile: {}\n".format(file)
    desc += "-size: {}\n" \
            "-datas[0] demo:\n".format(len(Handler.datas))
    desc += "\t-.id: {}\n" \
            "\t-.text: {}\n" \
            "\t-.aspect_terms: {}\n" \
            "\t-.aspect_categories: {}\n".format(Handler.datas[0].id,
                                                 Handler.datas[0].text,
                                                 Handler.datas[0].aspect_terms,
                                                 Handler.datas[0].aspect_categories)
    return Handler.datas, desc


def term_replacement(text, aspect_terms, join=False):

    # text: str
    # aspect_terms: [(aspect_term, (from, to), polarity)...]

    placeholders = [] # [str]
    ap_terms = [] # [str]
    positions = [] # [(from, to)]

    for t in aspect_terms: # aspect terms inside one text
        # t: (aspect_term, (from, to), polarity)
        aspect_term = t[0]
        polarity = t[2]
        term_size = len(aspect_term.split())

        # create place holder for every term
        ph = placeholder_constructor(term_size, polarity, join=join)
        placeholders.append(ph)
        ap_terms.append(aspect_term)
        positions.append(t[1])

    assert len(placeholders) == len(ap_terms)

    if len(placeholders) > 0:
        text_ph = washer(replace_with_index(text=text,
                                             placeholders=placeholders,
                                             positions=positions)) # "...$B-POS$ $I-POS$..."
        ap_terms = ",".join(ap_terms)
    else:
        text_ph = washer(text)
        ap_terms = None

    return text_ph, ap_terms

def aspect_category_constructor(categories):

    # aspect_categories: [category]
    category_size = len(categories)

    if category_size > 0:
        output = ",".join(set(categories))
    else:
        output = None

    return output

def SE14_ATEDataPrepare(file, join, rm_none_aspect=False):

    # file: data file path
    # rm_none_aspect: remove text without aspect terms

    datas, _ = SemEval14XMLReader(file=file)
    # datas: [data/.id/.text/.aspect_terms/.aspect_categories]
    outputs = []
    for data in datas:
        text = data.text
        aspect_terms = data.aspect_terms
        aspect_categories = data.aspect_categories

        if aspect_terms is not None:
            # "All the $B-POS$ and $B-POS$ were fabulous, the $B-POS$ was mouth watering and the $B-POS$ was delicious!!!"
            text_ph, ap_terms = term_replacement(text, aspect_terms, join=join)
            label = label_constructor(text_ph) # "...$B-POS$ $I-POS$..."
            ap_categories = aspect_category_constructor(aspect_categories) if aspect_categories is not None else None
            outputs.append([text_ph, label, ap_terms, ap_categories])

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

####################################################################################################################

def SemEval2014_AspectTerm(file_name, join, rm_none_aspect=False):

    type = "jte" if join else "ate"
    for k, v in file_name.items():

        datas = SE14_ATEDataPrepare(file=v,
                                    join=join,
                                    rm_none_aspect=rm_none_aspect)
        desc = ">>> {} \n" \
               "\t- size: {} \n" \
               "\t- sample: {} \n".format(k,
                                          len(datas),
                                          datas[0])
        print(desc)
        # write to csv file
        with codecs.open("resources/AspectTermExtraction/{}-{}.csv".format(k, type), "w", "utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(datas)