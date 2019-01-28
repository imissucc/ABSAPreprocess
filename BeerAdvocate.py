import os
import csv
import random
import codecs


def beeravocate_data_constructor(dataset="beeradvocate"):
    from_dirpath = os.path.join("datasets", dataset)
    to_dirpath = os.path.join("resources/AspectExtraction", dataset)

    train_fname = os.path.join(to_dirpath, "train.csv")
    test_fname = os.path.join(to_dirpath, "test.csv")

    if (not os.path.exists(train_fname)) or (not os.path.exists(test_fname)):
        desc = ">>> constructing beeradvocate dataset...\n"

        # dirpath init
        if not os.path.exists(to_dirpath):
            os.mkdir(to_dirpath)

        # read train data
        train_data = list()
        fname = os.path.join(from_dirpath, "train.txt")
        with codecs.open(fname, "r", "utf-8") as file:
            for line in file.readlines():
                if len(line) > 10:
                    row = []
                    row.append(line.strip())
                    train_data.append(row)

        # read test data
        test_data = list()
        test_text = list()
        test_label = list()
        textfile = os.path.join(from_dirpath, "test.txt")
        labelfile = os.path.join(from_dirpath, "test_label.txt")

        # read from text file
        with codecs.open(textfile, "r", "utf-8") as text_file:
            for line in text_file.readlines():
                test_text.append(line.strip())
        # read from label file
        with codecs.open(labelfile, "r", "utf-8") as label_file:
            for line in label_file.readlines():
                test_label.append(line.strip())

        for i in range(len(test_text)):
            row = []
            row.append(test_label[i])
            row.append(test_text[i])
            test_data.append(row)

        desc += "\t- train data: {}\n" \
                "\t- test data: {}\n".format(len(train_data), len(test_data))

        # write train csv file
        with codecs.open(train_fname, "w+", "utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(train_data)
        # write train csv file
        with codecs.open(test_fname, "w+", "utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(test_data)

    else:
        desc = ">>> beeradvocate dataset exists..."

    print(desc)

if __name__ == "__main__":

    beeravocate_data_constructor()