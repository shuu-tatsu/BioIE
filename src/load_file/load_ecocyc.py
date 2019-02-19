target_file = '/cl/work/shusuke-t/BioIE/2019_02_05_data_nomura/gene/ecocyc/'
read_file = target_file + 'All_genes_of_E._coli_K-12_substr._MG1655.txt'
write_file = target_file + 'gene_ecocyc.txt'

with open(read_file, 'r') as r:
    word_list = [l for l in r]

with open(write_file, 'w') as w:
    for word_tsv in word_list[1:]:
        gene = word_tsv.split()[0]
        w.write(gene[1:-1])
        w.write('\n')
