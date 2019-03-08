#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ErrorAnalyzer():

    def __init__(self, sentences_list):
        self.sentences_list = sentences_list

    def analyze(self):
        self.fp_error_sentences_list = []
        self.fn_error_sentences_list = []
        for sentence in self.sentences_list:
            if find_fp_error(sentence):
                self.fp_error_sentences_list.append(sentence)
            if find_fn_error(sentence):
                self.fn_error_sentences_list.append(sentence)

    def get_fp_error_sentences_list(self):
        return self.fp_error_sentences_list

    def get_fn_error_sentences_list(self):
        return self.fn_error_sentences_list


def find_fp_error(sentence):
    return find_error(sentence.words_list, 'fp')


def find_fn_error(sentence):
    return find_error(sentence.words_list, 'fn')


def find_error(words_list, error_type_str):
    for word_str in words_list:
        word_cls = Word()
        if word_cls.error_analyze(word_str) == error_type_str:
            return True
    return False


class Word():

    def __init__(self):
        pass

    def error_analyze(self, word):
        token_list = word.split()
        gold_tag = token_list[-2]
        pred_tag = token_list[-1]
        return self.type_decision(gold_tag, pred_tag)

    def type_decision(self, gold_tag, pred_tag):
        if gold_tag != pred_tag:
            if gold_tag == 'O':
                return 'fp'
            elif pred_tag == 'O':
                return 'fn'
            else:
                return None


class Loader():

    def __init__(self):
        pass

    def read_file(self, read_file):
        with open(read_file, 'r') as r:
            read_data = [word for word in r]
        return read_data

    def extract_sentence(self, words_list):
        eos_index_list = find_eos(words_list)
        # sentences_list consists of Sentence classes
        sentences_list = split_sentences_list(words_list, eos_index_list)
        return sentences_list


def split_sentences_list(words_list, eos_index_list):
    sentences_list = []
    s_index = 0
    for i in range(len(eos_index_list)):
        e_index = eos_index_list[i]
        one_sentence = Sentence(words_list[s_index:e_index])
        sentences_list.append(one_sentence)
        s_index = e_index + 1
    return sentences_list


def find_eos(words_list):
    eos_index_list = []
    for index, word in enumerate(words_list):
        token_list = word.split()
        if len(token_list) > 1 and token_list[0] == '.':
            next_index = index + 1
            if words_list[next_index] == '\n':
                eos_index_list.append(next_index)
    return eos_index_list


class Sentence():

    def __init__(self, one_sentence_list):
        self.words_list = one_sentence_list
        self.size = len(self.words_list)

    def print_text(self):
        print(self.words_list)


def data_writing(write_file, error_list):
    with open(write_file, 'w') as w:
        for error in error_list:
            # error is Sentence object
            for word in error.words_list:
                w.write(word)
            w.write('\n')


def main(read_file, fp_write_file, fn_write_file):
    # Data Loading
    loader = Loader()
    words_list = loader.read_file(read_file)
    sentences_list = loader.extract_sentence(words_list)

    # Data Analysis
    analyser = ErrorAnalyzer(sentences_list)
    analyser.analyze()
    fp_list = analyser.get_fp_error_sentences_list()
    fn_list = analyser.get_fn_error_sentences_list()

    # Data writing
    data_writing(fp_write_file, fp_list)
    data_writing(fn_write_file, fn_list)


if __name__ == '__main__':
    # Data
    read_file = '/cl/work/shusuke-t/flair_myLM_normal/resources/taggers/BioIE/bio_multi_label_0306manual_all_ne/test.tsv'
    fp_write_file = '/cl/work/shusuke-t/flair_myLM_normal/resources/taggers/BioIE/bio_multi_label_0306manual_all_ne/fp_error.txt'
    fn_write_file = '/cl/work/shusuke-t/flair_myLM_normal/resources/taggers/BioIE/bio_multi_label_0306manual_all_ne/fn_error.txt'
    main(read_file, fp_write_file, fn_write_file)
