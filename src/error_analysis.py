#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ErrorAnalyser():

    def __init__(self, all_sent_list):
        self.all_sent_list = all_sent_list
        self.pre_error_list = []
        self.rec_error_list = []

    def discriminate(self):
        for one_sent_list in self.all_sent_list:
            if self.find_error(one_sent_list):
                '''
                error_type: ['pre', 'rec', 'both']
                '''
                error_type = self.get_error_type(one_sent_list)
                self.classify(one_sent_list, error_type)
            else:
                pass

    def find_error(self, one_sent_list):
        for word in one_sent_list:
            gold = word.split(' ')[1]
            pred = word.split(' ')[2].strip()
            if gold != pred:
                return True
        return False

    def get_error_type(self, one_sent_list):
        pre_error = 0
        rec_error = 0
        for word in one_sent_list:
            gold = word.split(' ')[1]
            pred = word.split(' ')[2].strip()
            # precision error
            if pred == 'B-CHEMICAL' or pred == 'I-CHEMICAL':
                if gold == 'O':
                    pre_error = 1
            # recall error
            if gold == 'B-CHEMICAL' or gold == 'I-CHEMICAL':
                if pred == 'O':
                    rec_error = 1
        if pre_error + rec_error == 2:
            return 'both'
        elif pre_error == 1 and rec_error == 0:
            return 'pre'
        elif rec_error == 1 and pre_error == 0:
            return 'rec'
        else:
            return None

    def classify(self, one_sent_list, error_type):
        if error_type == 'pre':
            self.pre_error_list.append(one_sent_list)
        elif error_type == 'rec':           
            self.rec_error_list.append(one_sent_list)
        elif error_type == 'both':
            self.pre_error_list.append(one_sent_list)
            self.rec_error_list.append(one_sent_list)
        else:
            pass

    def print_error(self, error_type, write_file):
        w = open(write_file, 'w')
        if error_type == 'pre':
            # Precision Error Sentences
            # False Positive
            w = self.printout(self.pre_error_list, w)
        elif error_type == 'rec':
            # Recall Error Sentences
            # False Negative
            w = self.printout(self.rec_error_list, w)
        else:
            pass
        w.close()

    def printout(self, error_list, w):
        for sent in error_list:
            for word in sent:
                w.write(word)
            w.write('\n')
        return w

def load(read_file):
    with open(read_file, 'r') as r:
        word_list = [word for word in r]
    return word_list


def separate(word_list):
    all_sent_list = []
    one_sent_list = []
    for i, word in enumerate(word_list):
        if find_eos(i, word, word_list):
            # this word is EOS
            one_sent_list.append(word)
            all_sent_list.append(one_sent_list)
            one_sent_list = []
        else:
            # this word is in sentence
            if len(one_sent_list) == 0:
                if word.split(' ')[0] != '\n':
                    # SOS should not be '\n'
                    one_sent_list.append(word)
            else:
                one_sent_list.append(word)
    return all_sent_list


def find_eos(index, word, word_list):
    token = word.split(' ')[0]
    if token == '.':
        next_word = word_list[index + 1]
        next_token = next_word.split(' ')[0]
        if next_token == '\n':
            return True
    return False


def main():
    # data
    #READ_FILE = '/cl/work/shusuke-t/flair_myLM_normal/resources/taggers/BioIE/bio01_insense/test.tsv'
    #READ_FILE = '/cl/work/shusuke-t/flair_myLM_normal/resources/taggers/BioIE/bio02_sense/test.tsv'
    READ_FILE = '/cl/work/shusuke-t/flair_myLM_normal/resources/taggers/BioIE/bio01_insense/toy.tsv'
    WRITE_FILE_PRE = '/cl/work/shusuke-t/BioIE/data/error_analysis/fp_error.txt'
    WRITE_FILE_REC = '/cl/work/shusuke-t/BioIE/data/error_analysis/fn_error.txt'

    # preparing data
    word_list = load(READ_FILE)
    all_sent_list = separate(word_list)

    # analysing data
    analyser = ErrorAnalyser(all_sent_list)
    analyser.discriminate()
    analyser.print_error('pre', WRITE_FILE_PRE)
    analyser.print_error('rec', WRITE_FILE_REC)


if __name__ == '__main__':
    main()
