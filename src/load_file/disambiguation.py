gene = '/cl/work/shusuke-t/BioIE/2019_02_05_data_nomura/gene/ecocyc/gene_ecocyc.txt'
protein = '/cl/work/shusuke-t/BioIE/2019_02_12_parse_drugbank_ipynb/data/protein_drugbank.txt'

with open(gene, 'r') as r:
    gene_set = set([w for w in r])

with open(protein, 'r') as r:
    protein_set = set([w for w in r])

intersection = gene_set & protein_set
print(intersection)
