import xml.sax


class SemEval14Data:

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
    def aspect_terms(self):
        return self._aspect_terms

    @aspect_terms.setter
    def aspect_terms(self, value):
        assert isinstance(value, list)
        self._aspect_terms = value

    @property
    def aspect_categories(self):
        return self._aspect_terms

    @aspect_categories.setter
    def aspect_categories(self, value):
        assert isinstance(value, list)
        self_aspect_categories = value

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
            polarity = attributes["polarity"]
            fromto = (int(attributes["from"]), int(attributes["to"]))
            self.aspect_terms.append((term, polarity, fromto))
        elif tag == "aspectCategory":
            # category data
            category = attributes["category"]
            polarity = attributes["polarity"]
            self.aspect_categories.append((category, polarity))

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
            self.data.aspect_terms = self.aspect_terms
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

if __name__ == "__main__":

    datas, desc = SemEval14XMLReader("data/restaurants-trial.xml")

    print(desc)