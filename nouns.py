from glob import glob
import os
import sys
import MeCab

DATETIME_CHARS = '0123456789:./'

class NounsConv(object):
    """docstring for NounsConv"""
    def __init__(self):
        super(NounsConv, self).__init__()
        self.mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

    def run(self, rootdir):
        sub_dirs = glob(os.path.join(rootdir, '*'))

        for sub in sub_dirs:
            files = glob(os.path.join(sub, '*.txt'))
            for filename in files:
                self.convert(filename)

    def exclude(self, text):
        if len(text) <= 0:
            return True
        if all((c in DATETIME_CHARS for c in text)):
            # print('Exclude: ' + text)
            return True
        return False

    def exclude_component(self, components):
        if components[1] != '名詞':
            # print('Exclude: ' + str(components))
            return True
        if components[2] in ('数'):
            # print('Exclude: ' + str(components))
            return True

        return False

    def convert(self, filename):
        print('File: ' + filename)
        nouns = []
        with open(filename, 'r') as text_file:
            name = os.path.splitext(filename)[0]
            for line in text_file.readlines():
                line = line.strip()
                if not self.exclude(line):
                    nouns.extend(self.parse_sentence(line))
        with open(name + '.noun', 'w') as noun_file:
            noun_file.write(' '.join(nouns))

    def parse_sentence(self, sentence):
        nouns = []
        res = self.mecab.parse(sentence)
        for item in res.split('\n'):
            components = item.split('\t')
            if components[0] == 'EOS' or len(components) < 2:
                continue
            word = components[0]
            components = components[1].split(',')
            components.insert(0, word)
            if not self.exclude_component(components):
                print(components[0])
                nouns.append(components[0])
        return nouns

if __name__ == '__main__':
    conv = NounsConv()
    conv.run(sys.argv[1])
