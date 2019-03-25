import config
import utils


class Dictionary():

    def __init__(self, file_path, label_str):
        self.label_str = label_str
        self.vocab_list = self.load(file_path)

    def load(self, file_path):
        with open(file_path, 'r') as r:
            word_list = [utils.preprocessing(w.strip()) for w in r]
        return word_list

    def search_index_word(self, word, table):
        # search B
        if table.index_id == 0:
            pred_label, table = self.search(word, table, 'B')

        # judge I or Not. if Not: continue search B
        else:
            pred_label, table = self.search(word, table, 'I')
        return pred_label, table

    def search(self, word, table, tag):
        for word_id, v in enumerate(self.vocab_list):
            if tag == 'I':
                if word_id in table.pre_word_id_list:
                    try:
                        if word == v[table.index_id]:
                            table.new_word_id_list.append(word_id)
                    except IndexError:
                        pass
            elif tag == 'B':
                try:
                    if word == v[table.index_id]:
                        table.new_word_id_list.append(word_id)
                except IndexError:
                    pass

        if len(table.new_word_id_list) > 0:
            table.index_id += 1
            pred_label = tag + '-' + self.label_str.upper()
            table.update_word_id_list()
        else:
            table.init_id()
            if tag == 'I':
                pred_label, table = self.search(word, table, 'B')
            elif tag == 'B':
                pred_label = 'O'
        return pred_label, table

