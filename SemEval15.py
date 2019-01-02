import xml.sax


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
        assert isinstance(value, list)
        self._opinions = value


class SemEval15Review:

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        assert isinstance(value, str)
        self._id = value

    @property
    def sentences(self):
        return self._sentences

    @sentences.setter
    def sentences(self, value):
        assert isinstance(value, list)
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
            self.opinions.append((attributes["target"], attributes["category"], attributes["polarity"], (attributes["from"], attributes["to"])))

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

if __name__ == "__main__":

    datas, desc = SemEval15XMLReader("data/absa-2015_restaurants_trial.xml")

    print(desc)