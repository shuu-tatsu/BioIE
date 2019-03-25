import re


def preprocessing(sentence):
    sentence = sentence.replace(')', ' ) ')
    sentence = sentence.replace('(', ' ( ')
    sentence = sentence.replace('-', ' - ')
    sentence = sentence.replace(', ', ' , ')
    sentence = sentence.replace('. ', ' . ')
    sentence = sentence.replace('; ', ' ; ')
    sentence = sentence.replace('.\n', ' . ')
    sentence = re.split('\s+', sentence)
    return sentence


def main():
    # sample
    token = preprocessing('putative D,D-dipeptide ABC transporter ATP-binding subunit DdpD')
    print(token)
    for t in token:
        print('{} I-PROTEIN'.format(t))

if __name__ == '__main__':
    main()
