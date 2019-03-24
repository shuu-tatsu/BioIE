import vocab
import config


def match(line_list, dict_list):
    for line in line_list:
        split_line = line.split(' ')
        if len(split_line) == 2:
            word = split_line[0]
            gold_label = split_line[1]
            pred_label = search_dict(word, dict_list)
        elif len(split_line) > 2:
            print('warning')


def search_dict(word, dict_list):
    for dic in dict_list:
        dic.search_index_word(query_index=1)
    


def load(test_file):
    with open(test_file, 'r') as r:
        line_list = [line for line in r]
    return line_list


def main():
    # prepare test data
    test_file = config.test_data
    line_list = load(test_file)

    # prepare dict
    dict_list = []
    for i, d in enumerate(config.dict_list):
        file_path = d[0]
        label_str = d[1]
        dic = vocab.Dictionary(file_path, label_str)
        dict_list.append(dic)

    # matching
    match(line_list, dict_list)


if __name__ == '__main__':
    main()
