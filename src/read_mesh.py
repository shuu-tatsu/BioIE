import xml.etree.ElementTree as ET

# ファイルの内容でtreeを初期化
tree = ET.ElementTree(file='MeSHdesc2018_nomura')

# treeのroot要素を取得
root = tree.getroot()

# XMLの構造体の中に順に潜って要素を取得
for fruits in root:
    #indent 0: 一つのMeshTermを管理するレイヤー
    for fruit in fruits:
        #indent1: DescriptorName
        if fruit.tag == 'DescriptorName':
            for name in fruit:
                if name.tag == 'String':
                    mesh_term = name.text
        for items in fruit:
            #indent2: String in DescriptorName MeshTerm
            for item in items:
                #indent6
                if item.tag == 'TermList':
                    for terms in item:
                        for term in terms:
                            if term.tag == 'String':
                                extracted_word = term.text
                                print('{}	{}'.format(extracted_word, mesh_term))
