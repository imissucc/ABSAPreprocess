import xml.sax
import csv
import codecs

from utils import *


class SemEval15Sentence:

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
        assert isinstance(value, str)
        self._text = value

    @property
    def opinions(self):
        return self._opinions

    @opinions.setter
    def opinions(self, value):
        # assert isinstance(value, list)
        self._opinions = value


class SemEval15Review:

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def sentences(self):
        return self._sentences

    @sentences.setter
    def sentences(self, value):
        self._sentences = value

class SemEval15Handler(xml.sax.ContentHandler):

    def __init__(self):

        super(SemEval15Handler, self).__init__()
        self.CurrentTag = None
        self.datas = []

        self.rid = None
        self.sid = None
        self.text = None
        self.opinions = None

        self.sentences = None

    def startElement(self, tag, attributes):

        self.CurrentTag = tag
        if tag == "Review":
            self.review = SemEval15Review()
            self.review.id = attributes["rid"]
        elif tag == "sentences":
            self.sentences = []
        elif tag == "sentence":
            self.sentence = SemEval15Sentence()
            self.sid = attributes["id"]
        elif tag == "Opinions":
            self.opinions = []
        elif tag == "Opinion":
            self.opinions.append((attributes["target"], attributes["category"], attributes["polarity"], (int(attributes["from"]), int(attributes["to"]))))

    def characters(self, content):

        if self.CurrentTag == "text":
            self.text = content

    def endElement(self, tag):

        if tag == "text":
            self.sentence.text = self.text
        elif tag == "sentence":
            self.sentence.id = self.sid
            self.sentence.opinions = self.opinions
            self.sentences.append(self.sentence)
        elif tag == "Review":
            self.review.sentences = self.sentences
            self.datas.append(self.review)

def SemEval15XMLReader(file):

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = SemEval15Handler()
    parser.setContentHandler(Handler)

    parser.parse(file)

    desc = ">>> datafile: {}\n".format(file)
    desc += "-size: {}\n" \
            "-datas[0] demo:\n".format(len(Handler.datas))
    desc += "\t-.id (review id): {}\n" \
            "\t-.sentences: {}\n" \
            "\t-sentences size: {}\n".format(Handler.datas[0].id,
                                           Handler.datas[0].sentences,
                                           len(Handler.datas[0].sentences))
    desc += "\t-sentences[0] demo:\n" \
            "\t\t-.id (sentence id): {}\n" \
            "\t\t-.text: {}\n" \
            "\t\t-.opinions: {}\n".format(Handler.datas[0].sentences[0].id,
                                          Handler.datas[0].sentences[0].text,
                                          Handler.datas[0].sentences[0].opinions)
    return Handler.datas, desc

def term_replacement(text, opinions, join=False):

    # text: str
    # opinions: [(term, entity#attribute, polarity, (from, to))...]

    placeholders = [] # place holder terms
    ap_terms = [] # aspect terms
    categories = [] # categories
    ap_map = {}  # dict[position] = (aspect_term, placeholder)

    for t in opinions:
        # t: (term, entity#attribute, polarity, (from, to))
        aspect_term = t[0] # maybe == "NULL"
        position = t[3]
        polarity = t[2]
        if aspect_term != "NULL":
            term_size = len(aspect_term.split())
            # create place holder for every term
            ph = placeholder_constructor(term_size, polarity, join=join)
            placeholders.append(ph)
            ap_terms.append(aspect_term)
            ap_map[position] = (aspect_term, ph)

        categories.append(t[1])

    ap_sorted = dict(sorted(ap_map.items(), key=lambda i: i[0][0]))

    # if aspect_terms is not None
    assert len(placeholders) == len(ap_terms)

    if len(placeholders) > 0:
        text_ph = replace_with_index(text=text,
                                     aspect_map=ap_sorted)
        text_ph = washer(text_ph) # "...$B-POS$ $I-POS$..."
        text = placeholder_reverse(text_ph=text_ph,
                                   aspect_map=ap_map)
        ap_terms = ",".join(ap_terms)
    else: # text without aspect term
        text_ph = text = washer(text)
        ap_terms = None

    if len(categories) > 0:
        categories = ",".join(set(categories))
    else:
        categories = None

    return text, text_ph, ap_terms, categories

def SE15_ATEDataPrepare(file, join, rm_none_aspect=False):

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
            text, text_ph, ap_terms, ap_categories = term_replacement(text, opinions, join=join)
            label = label_constructor(text_ph)

            # if ignore sentences without aspect
            if rm_none_aspect and ap_terms is None:
                continue
            outputs.append([text, label, ap_terms, ap_categories])

    return outputs


####################################################################################################################

def SemEval2015_AspectTerm(file_name, join, rm_none_aspect=False):

    type = "jte" if join else "ate"

    for k, v in file_name.items():

        datas = SE15_ATEDataPrepare(file=v,
                                    join=join,
                                    rm_none_aspect=rm_none_aspect)

        origin_size = len(datas)
        pop_list = verifier(datas=datas)

        for i in pop_list:
            datas.pop(i)

        desc = ">>> {} \n" \
               "\t- origin size: {} \n" \
               "\t- verified size: {} \n" \
               "\t- pop count: {} \n" \
               "\t- sample: {} \n".format(k,
                                          origin_size,
                                          len(datas),
                                          len(pop_list),
                                          datas[0])

        print(desc)
        # write to csv file
        with codecs.open("resources/AspectTermExtraction/{}-{}.csv".format(k, type), "w", "utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(datas)