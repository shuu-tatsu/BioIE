target_file = '/cl/work/shusuke-t/BioIE/2019_02_12_parse_drugbank_ipynb/data/'
read_file = target_file + 'drugbank.tsv'
write_file = target_file + 'protein_drugbank.txt'

with open(read_file, 'r') as r:
    word_list = [l for l in r]

with open(write_file, 'w') as w:
    for word_tsv in word_list[1:]:
        drugbank_id = word_tsv.split('\t')[0]
        if drugbank_id[0:2] == 'DB':
            protein_name = word_tsv.split('\t')[1]
            w.write(protein_name)
            w.write('\n')
