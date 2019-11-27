import gensim
import pymorphy2
from config import config


class Comparer:
    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format('binaries/ruwikiruscorpora_upos_skipgram_300_2_2019.bin',
                                                                     binary=True)
        self.model.init_sims(replace=True)
        # print(set(map(lambda x: x.split('_')[1], self.model.vocab.keys())))
        self.morph = pymorphy2.MorphAnalyzer()

    def get_neighbours(self, _word: str):
        return self.model.most_similar(_word)

    def get_lemma(self, _word: str) -> tuple:
        result = self.morph.parse(_word)
        return result[0].normal_form, self.get_type_for_model(str(result[0].tag)[:4])

    @staticmethod
    def get_type_for_model(_type: str) -> str:
        return config.types[_type]


if __name__ == '__main__':
    comparer = Comparer()
    # for word in ['сестры', 'сделали', 'него', 'красиво', 'красивого',
    #              'каждый', 'себя', 'он',
    #              'три',
    #              'от', 'а', 'не', 'более', 'еще', 'менее',
    #              'увы']:
    for word in input().split():
        lemma = comparer.get_lemma(word)
        if lemma[1]:
            lemma = '_'.join(lemma)
            try:
                print(comparer.get_neighbours(lemma))
            except KeyError:
                print(f'No suggestions to word {lemma.split("_")[0]}')
        else:
            lemma = lemma[0]
            print(f'No suggestions to word {lemma}')
        print(lemma)
        # print([x for x in comparer.model.vocab.keys() if x.startswith(lemma.split('_')[0])])
        print('-------------------------------------')
