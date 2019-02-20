#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import os
import os.path
import re


class Converter():

    def __init__(self, file_list):
        self.read_dir = file_list[0]
        self.id_data_dir = file_list[1]
        self.anno_data_dir = file_list[2]

    def convert(self):
        #read
        xhtml_list = self.read('.xhtml')
        htmlanno_list = self.read('.htmlanno')

        #write
        self.write_id(xhtml_list)
        self.write_anno(htmlanno_list)

    def read(self, ext_type):
        files = []
        for f in os.listdir(self.read_dir):
            if os.path.isfile(self.read_dir + f):
                root, ext = os.path.splitext(self.read_dir + f)
                if ext == ext_type:
                    files.append(f)
        return files

    def write_id(self, abst_list):
        '''
        <h1>[改行][タイトル][改行]</h1>[改行]<p>[改行]本文[改行]</p>
        '''
        #ファイル読み込み
        extracted_list = []
        for abst_file in abst_list:
            abst_id = abst_file[:abst_file.find('.')]

            with open(self.read_dir + abst_file, 'r') as r:
                xhtml_str = r.read()

            #HTMLを解析(BeautifulSoup)
            soup = BeautifulSoup(xhtml_str, 'html.parser')
            title_str = soup.html.body.h1
            abst_str = soup.html.body.p
            #改行をスペースに変換
            text_str = ('\n' + title_str.string + '\n' + abst_str.string).replace('\n',' ')
            extracted_list.append((abst_id, text_str))

        #ファイル書き込み
        id_data_file = 'id_test.txt'
        with open(self.id_data_dir + id_data_file, 'w') as w:
            for abst_id, text_str in extracted_list:
                written_str = abst_id + '\t' + text_str + '\n'
                w.write(written_str)

    def write_anno(self, anno_list):
        '''
        条件:
        type = "span"
        label = "gene" or "protein"
        '''
        extracted_anno_list = []
        for anno_file in anno_list:
            anno_id = anno_file[:anno_file.find('.')]
            with open(self.read_dir + anno_file, 'r') as r:
                anno_parser = AnnoParser(r)
                #one abst（同一anno_id）における、アノテーション情報
                anno_info_list = anno_parser.read()
            extracted_anno_list.append((anno_id, anno_info_list))

        #ファイル書き込み
        anno_data_file = 'anno_test.txt'
        with open(self.anno_data_dir + anno_data_file, 'w') as w:
            for abst_id, anno_info_list in extracted_anno_list:
                for anno_info in anno_info_list:
                    anno_type = anno_info[0][0]
                    position = anno_info[1][0]
                    try:
                        s_posi_temp = position.strip('[], ').split(',')[0]
                        e_posi_temp = position.strip('[], ').split(',')[1]
                        s_posi = min(s_posi_temp, e_posi_temp)
                        e_posi = max(s_posi_temp, e_posi_temp)
                    except IndexError:
                        s_posi = -1
                        e_posi = -1
                    ne_name = anno_info[2][0]
                    label = anno_info[3][0]
                    #条件でフィルタリング
                    if anno_type == 'span':
                        if label == 'gene' or label == 'protein':
                            written_str = abst_id + '\t' + ne_name + '\t' + \
                                          s_posi + '\t' + e_posi + '\t' + label + '\n'
                            w.write(written_str)


'''
AnnoParser
解析対象：abst 1つ
'''
class AnnoParser():

    def __init__(self, r):
        self.r = r

    def read(self):
        lines = [line for line in self.r]
        start_index_list = self.get_start_index(lines)
        tuple_index_list = self.get_tuple_index(start_index_list)
        extracted_info_list = self.parse(lines, tuple_index_list)
        return extracted_info_list

    def parse(self, lines, tuple_index_list):
        extracted_info_list = []
        for s_index, e_index in tuple_index_list:
            entity = lines[s_index:e_index]
            entity_info_list = []
            for anno_info in entity:
                info_str = re.sub('[\n\s"]', '', anno_info).split('=')[-1:]
                entity_info_list.append(info_str)
            extracted_info_list.append(entity_info_list)
        return extracted_info_list

    def get_tuple_index(self, start_index_list):
        tuple_index_list = [(s, s + 4) for s in start_index_list]
        return tuple_index_list

    def get_start_index(self, lines):
        start_index_list = []
        for i, line in enumerate(lines):
            if line.find('type') == 0:
                start_index_list.append(i)
        return start_index_list


def main():
    # data
    READ_DIR = '/cl/work/shusuke-t/BioIE/2019_02_05_data_nomura/manual_anno0220/'
    WRITE_DIR = '/cl/work/shusuke-t/BioIE/data/multi_label_corpus/manual/'
    ANNO_DATA_DIR = WRITE_DIR + 'anno_data/'
    ID_DATA_DIR = WRITE_DIR + 'id_data/'
    file_list = [READ_DIR, ID_DATA_DIR, ANNO_DATA_DIR]

    # convert
    converter = Converter(file_list)
    converter.convert()


if __name__ == '__main__':
    main()
