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
        self.datas = []

    def startElement(self, tag, attributes):

        self.CurrentTag = tag
        if tag == "aspectTerms":
            # reset
            self.aspect_terms = {}
        elif tag == "sentence":
            # reset data instance
            self.data = SemEval14Data()
            self.id = attributes["id"]
        elif tag == "aspectTerm":
            # term data
            term = attributes["term"]
            position = (int(attributes["from"]), int(attributes["to"]))
            polarity = attributes["polarity"]

            if position not in self.aspect_terms.keys():
                self.aspect_terms[position] = (term, polarity)
            else:
                # when the aspect_position is exists in opinions dictionary
                _polarity_exist = self.aspect_terms[position][1]
                _polarity = polarity_addition(_polarity_exist, polarity)
                self.aspect_terms[position] = (term, polarity)

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
            if self.aspect_terms is None or len(self.aspect_terms) > 0:
                self.data.aspect_terms = self.aspect_terms
            else: # is not None and len=0
                self.data.aspect_terms = None


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
    # aspect_terms: dict[(from, to)] = (term, polarity)

    placeholders = [] # [str]
    ap_terms = [] # [str]
    ap_map = {} # dict[position] = (aspect_term, placeholder)

    for position, (aspect_term, polarity) in aspect_terms.items():
        # aspect terms inside one text
        term_size = len(aspect_term.split())

        # create place holder for every term
        ph = placeholder_constructor(term_size, polarity, join=join)
        placeholders.append(ph)
        ap_terms.append(aspect_term)
        ap_map[position] = (aspect_term, ph)

    ap_sorted = dict(sorted(ap_map.items(), key=lambda i: i[0][0]))

    if len(placeholders) > 0:
        text_ph = replace_with_index(text=text,
                                     aspect_map=ap_sorted)
        text_ph = washer(text_ph) # "...$B-POS$ $I-POS$..."
        text = placeholder_reverse(text_ph=text_ph,
                                   aspect_map=ap_sorted)
        ap_terms = ",".join(ap_terms)
    else:
        text_ph = text = washer(text)
        ap_terms = None

    return text, text_ph, ap_terms

def aspect_category_constructor(categories):

    # aspect_categories: [category]
    category_size = len(categories)

    if category_size > 0:
        output = ",".join(set(categories))
    else:
        output = None

    return output

def SE14_ATEDataPrepare(file, join, rm_none_aspect=False, rm_conflicts=False):

    # file: data file path
    # rm_none_aspect: remove text without aspect terms

    datas, _ = SemEval14XMLReader(file=file)
    # datas: [data/.id/.text/.aspect_terms/.aspect_categories]
    outputs = []
    for data in datas:
        text = data.text
        aspect_terms = data.aspect_terms # dict[(from, to)] = (term, polarity)

        if aspect_terms is not None:
            conflict_keys = []
            if rm_conflicts:
                for key, (_, polarity) in aspect_terms.items():
                    if polarity == "conflict":
                        conflict_keys.append(key)
                for k in conflict_keys:
                    aspect_terms.pop(k)
                if len(aspect_terms) == 0:
                    aspect_terms = None

        if aspect_terms is not None :
            # "All the $B-POS$ and $B-POS$ were fabulous, the $B-POS$ was mouth watering and the $B-POS$ was delicious!!!"

            text, text_ph, ap_terms = term_replacement(text, aspect_terms, join=join)
            label = label_constructor(text_ph) # "...$B-POS$ $I-POS$..."
            outputs.append([text, label, ap_terms])

        else:
            if rm_none_aspect:
                continue
            else:
                # don't have aspect terms
                new_text = washer(text)
                text_label = label_constructor(new_text)
                ap_terms = None
                outputs.append([new_text, text_label, ap_terms])

    return outputs

####################################################################################################################

def SemEval2014_AspectTerm(file_name, join, rm_none_aspect=False, rm_conflicts=False):

    type = "jte" if join else "ate"
    con = "rc" if rm_conflicts else "nrc"

    for k, v in file_name.items():

        datas = SE14_ATEDataPrepare(file=v,
                                    join=join,
                                    rm_none_aspect=rm_none_aspect,
                                    rm_conflicts=rm_conflicts)
        origin_size = len(datas)
        datas, failed_count = verifier(datas=datas)

        desc = ">>> {} \n" \
               "\t- origin size: {} \n" \
               "\t- verified size: {} \n" \
               "\t- pop count: {} \n" \
               "\t- sample: {} \n".format(k,
                                          origin_size,
                                          len(datas),
                                          failed_count,
                                          datas[0])
        print(desc)
        # write to csv file
        with codecs.open("resources/AspectTermExtraction/{}-{}-{}.csv".format(k, type, con), "w", "utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(datas)