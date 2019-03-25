import vocab
import config


class IdTable():

    def __init__(self):
        self.new_word_id_list = []
        self.pre_word_id_list = []
        self.index_id = 0

    def update_word_id_list(self):
        self.pre_word_id_list = self.new_word_id_list
        self.new_word_id_list = []

    def init_id(self):
        self.new_word_id_list = []
        self.pre_word_id_list = []
        self.index_id = 0


def match(line_list, dic):
    table = IdTable()
    for line in line_list:
        split_line = line.strip().split(' ')
        if len(split_line) == 2:
            word = split_line[0]
            gold_label = split_line[1]
            pred_label, table = dic.search_index_word(word, table)
            print('{} {} {}'.format(word, gold_label, pred_label))
        elif len(split_line) > 2:
            print('warning')
        else:
            table.init_id()
            print('')


def load(test_file):
    with open(test_file, 'r') as r:
        line_list = [line for line in r]
    return line_list


def main():
    # prepare test data
    #test_file = config.test_data
    test_file = config.toy_data
    line_list = load(test_file)

    # prepare dict
    dict_list = []
    for i, d in enumerate(config.dict_list):
        file_path = d[0]
        label_str = d[1]
        dic = vocab.Dictionary(file_path, label_str)
        dict_list.append(dic)

    # matching
    for dic in dict_list:
        match(line_list, dic)


if __name__ == '__main__':
    main()
