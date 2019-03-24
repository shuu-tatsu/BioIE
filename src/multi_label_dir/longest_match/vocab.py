import config


class Dictionary():

   def __init__(self, file_path, label_str):
       self.label_str = label_str
       self.vocab_list = self.load(file_path)

   def load(self, file_path):
       with open(file_path, 'r') as r:
           word_list = [w.strip().split(' ') for w in r]
       return word_list

   def search_index_word(self, query_index):
       for v in self.vocab_list:
           try:
               print(v[query_index])
           except IndexError:
               pass

