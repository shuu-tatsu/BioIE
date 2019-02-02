#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tqdm import tqdm
from flashtext import KeywordProcessor
import random


class Annotation():

    def __init__(self, TRAIN_FILE, DEV_FILE, EVAL_FILE, DICT_FILE):
        self.train_file = TRAIN_FILE
        self.dev_file = DEV_FILE
        self.eval_file = EVAL_FILE
        self.dict_file = DICT_FILE

    def devide_vocab(self, rate=1):
        #Dictionary をソートし、rateに従ってtrain(devも供用)とevalに分ける。
        with open(self.dict_file, 'r') as r:
            words_duplication_list = [word.strip('\n') for word in r]
        words_list = remove_duplication(words_duplication_list)
        random.shuffle(words_list)
        self.train_vocab_list = words_list
        self.dev_vocab_list = words_list
        self.eval_vocab_list = words_list

    def make_annotation(self):
        make_anno_corpus(self.train_vocab_list, self.train_file)
        make_anno_corpus(self.dev_vocab_list, self.dev_file)
        make_anno_corpus(self.eval_vocab_list, self.eval_file)


def make_anno_corpus(vocab_list, target_corpus):
    #NE抽出器生成
    keyword_processor = make_ne_founder(vocab_list)
    #データからNEを抽出
    extracted_words_list = extract_keywords(target_corpus, keyword_processor) 
    #Write annotation file
    write_file = target_corpus[:37] + 'anno_data/anno_' + target_corpus[48:]
    write_annotation(extracted_words_list, write_file)


def write_annotation(extracted_words_list, write_file):
    with open(write_file, 'w') as w:
        for sent_id, keywords_found_list in extracted_words_list:
            for keywords_found in keywords_found_list:
                w.write(sent_id + '\t')
                w.write(str(keywords_found[0]) + '\t')
                w.write(str(keywords_found[1]) + '\t')
                w.write(str(keywords_found[2]))
                w.write('\n')


def make_ne_founder(vocab_list):
    keyword_processor = KeywordProcessor(case_sensitive=True)
    for vocab in tqdm(vocab_list):
        keyword_processor.add_keyword(vocab)
    return keyword_processor


def extract_keywords(target_corpus, keyword_processor):
    with open(target_corpus, 'r') as r:
        sentences = [sentence.split('\t') for sentence in r]
    extracted_words_list = []
    for sent_id, sentence in tqdm(sentences):
        keywords_found_list = keyword_processor.extract_keywords(sentence, span_info=True)
        extracted_words_list.append((sent_id, keywords_found_list))
    return extracted_words_list


def remove_duplication(words_list):
    words_set = set(words_list)
    words_noduplication_list = [word for word in words_set]
    return words_noduplication_list


def labeling_id(target_file, train_file, dev_file, eval_file):
    file_list = [train_file, dev_file, eval_file]
    for data_file in file_list:
        write_file = target_file + 'id_data/id_' + data_file[(len(target_file)+5):]
        with open(data_file, 'r') as r, open(write_file, 'w') as w:
            sentence_id = 1
            for sentence in r:
                line = str(sentence_id) + '\t' + sentence
                w.write(line)
                sentence_id += 1


def main(TARGET_FILE, DICT_FILE):
    make_id_corpus = True
    if make_id_corpus:
        TRAIN_FILE = TARGET_FILE + 'orig/train.txt' 
        DEV_FILE = TARGET_FILE + 'orig/valid.txt'
        EVAL_FILE = TARGET_FILE + 'orig/test.txt'
        labeling_id(TARGET_FILE, TRAIN_FILE, DEV_FILE, EVAL_FILE)

    make_anno_corpus = True
    if make_anno_corpus:
        TRAIN_FILE = TARGET_FILE + 'id_data/id_train.txt' 
        DEV_FILE = TARGET_FILE + 'id_data/id_valid.txt'
        EVAL_FILE = TARGET_FILE + 'id_data/id_test.txt'

        anno = Annotation(TRAIN_FILE, DEV_FILE, EVAL_FILE, DICT_FILE)
        anno.devide_vocab()
        anno.make_annotation()


if __name__ == '__main__':
    TARGET_FILE = '/cl/work/shusuke-t/BioIE/data/corpus/'
    DICT_FILE = '/cl/work/shusuke-t/BioIE/data/dict/vocab.txt'
    main(TARGET_FILE, DICT_FILE)
