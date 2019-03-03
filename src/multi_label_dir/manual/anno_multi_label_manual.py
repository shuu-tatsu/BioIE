#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tqdm import tqdm
from flashtext import KeywordProcessor
import random


class Annotation():

    #def __init__(self, TRAIN_FILE, DEV_FILE, EVAL_FILE, dict_list):
    def __init__(self, TRAIN_FILE, DEV_FILE, dict_list):
        self.train_file = TRAIN_FILE
        self.dev_file = DEV_FILE
        #self.eval_file = EVAL_FILE
        self.gene_list = self.load(dict_list[0])
        self.chemical_list = self.load(dict_list[1])

    def load(self, dict_file):
        with open(dict_file, 'r') as r:
            vocab_list = [word.strip('\n') for word in r]
        return vocab_list

    def make_annotation(self):
        make_anno_corpus(self.gene_list, self.chemical_list, self.train_file)
        make_anno_corpus(self.gene_list, self.chemical_list, self.dev_file)
        #make_anno_corpus(self.gene_list, self.chemical_list, self.eval_file)


def make_anno_corpus(gene_list, chemical_list, target_corpus):
    #NE抽出器生成
    #遺伝子は大文字小文字の区別あり、タンパク質は区別なし
    gene_processor = make_ne_founder(gene_list, case=True)
    chemical_processor = make_ne_founder(chemical_list, case=False)
    #データからNEを抽出
    extracted_words_list = extract_keywords(target_corpus, gene_processor, chemical_processor) 
    #Write annotation file
    write_file = target_corpus[:56] + 'anno_data/anno_' + target_corpus[67:]
    write_annotation(extracted_words_list, write_file)


def write_annotation(extracted_words_list, write_file):
    with open(write_file, 'w') as w:

        #all sentences
        for keywords_found_list in extracted_words_list:

            #one sentence
            for sent_id, keyword_found, tag_type in keywords_found_list:
                w.write(sent_id + '\t')
                w.write(str(keyword_found[0]) + '\t')
                w.write(str(keyword_found[1]) + '\t')
                w.write(str(keyword_found[2]) + '\t')
                w.write(tag_type)
                w.write('\n')


def make_ne_founder(vocab_list, case):
    keyword_processor = KeywordProcessor(case_sensitive=case)
    for vocab in tqdm(vocab_list):
        keyword_processor.add_keyword(vocab)
    return keyword_processor


def extract_keywords(target_corpus, gene_processor, chemical_processor):
    with open(target_corpus, 'r') as r:
        sentences = [sentence.split('\t') for sentence in r]
    extracted_words_list = []
    for sent_id, sentence in tqdm(sentences):
        gene_found_list = gene_processor.extract_keywords(sentence, span_info=True)
        chemical_found_list = chemical_processor.extract_keywords(sentence, span_info=True)

        sorted_list = sort_list(sent_id, gene_found_list, chemical_found_list)
        extracted_words_list.append(sorted_list)
    return extracted_words_list


def sort_list(sent_id, gene_found_list, chemical_found_list):
    #同一センテンス内でのソート
    temp_list = []
    temp_list.extend([(sent_id, gene_found, 'gene') for gene_found in gene_found_list])
    temp_list.extend([(sent_id, chemical_found, 'chemical') for chemical_found in chemical_found_list])
    sorted_list = sorted(temp_list, key=lambda x: x[1][1])
    return sorted_list


#def labeling_id(target_file, train_file, dev_file, eval_file):
def labeling_id(target_file, train_file, dev_file):
    #file_list = [train_file, dev_file, eval_file]
    file_list = [train_file, dev_file]
    for data_file in file_list:
        write_file = target_file + 'id_data/id_' + data_file[(len(target_file)+5):]
        with open(data_file, 'r') as r, open(write_file, 'w') as w:
            sentence_id = 1
            for sentence in r:
                line = str(sentence_id) + '\t' + sentence
                w.write(line)
                sentence_id += 1


def main(TARGET_FILE, dict_list):
    make_id_corpus = True
    if make_id_corpus:
        TRAIN_FILE = TARGET_FILE + 'orig/train.txt' 
        DEV_FILE = TARGET_FILE + 'orig/valid.txt'
        #EVAL_FILE = TARGET_FILE + 'orig/test.txt'
        #labeling_id(TARGET_FILE, TRAIN_FILE, DEV_FILE, EVAL_FILE)
        labeling_id(TARGET_FILE, TRAIN_FILE, DEV_FILE)

    make_anno_corpus = True
    if make_anno_corpus:
        TRAIN_FILE = TARGET_FILE + 'id_data/id_train.txt' 
        DEV_FILE = TARGET_FILE + 'id_data/id_valid.txt'
        #EVAL_FILE = TARGET_FILE + 'id_data/id_test.txt'

        #anno = Annotation(TRAIN_FILE, DEV_FILE, EVAL_FILE, dict_list)
        anno = Annotation(TRAIN_FILE, DEV_FILE, dict_list)
        anno.make_annotation()


if __name__ == '__main__':
    #TARGET_FILE = '/cl/work/shusuke-t/BioIE/data/multi_label_corpus/dsv/'
    TARGET_FILE = '/cl/work/shusuke-t/BioIE/data/multi_label_corpus/manual/'
    GENE = '/cl/work/shusuke-t/BioIE/2019_02_05_data_nomura/gene/ecocyc/gene_ecocyc.txt'
    CHEM = '/cl/work/shusuke-t/BioIE/2019_02_12_parse_drugbank_ipynb/data/drugbank.txt'
    dict_list = [GENE, CHEM]
    main(TARGET_FILE, dict_list)
