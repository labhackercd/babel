from nltk.corpus import floresta
from functools import lru_cache
from apps.nlp.pre_processing import stemmize
import nltk


@lru_cache()
def simplify_tag(tag):
    if "+" in tag:
        return tag[tag.index("+") + 1:]
    else:
        return tag


@lru_cache()
def default_stopwords():
    twords = floresta.tagged_words()
    stopwords = nltk.corpus.stopwords.words('portuguese')
    stopwords += [',', '.', 'srs', 'sr.', 'sra.', 'deputado', 'presidente',
                  'é', ':', "''", '`', '!', '``', '?', 'nº', 's.a.', 'quero',
                  'grande', 'dia', 'disse', 'pode', 'nesta', 'vamos', 'vai',
                  'vez', 'sras', 'dizer', 'falar', 'dar', 'chegou', 'mostrar',
                  'desses', 'coloca', 'deixou', '%', 'coisa', 'acharam',
                  'ficar', 'v.exa.', 'conclusao']

    valid_tags = ['adj', 'n', 'prop', 'nprop', 'est', 'npro', 'v-fin', 'v-inf',
                  'v-ger', 'v-pcp', 'vaux', 'v', 'vp', 'pcp', 'num']
    for (word, tag) in twords:
        tag = simplify_tag(tag)
        words = word.casefold().split('_')
        if tag not in valid_tags:
            stopwords += words

    return list(set(stopwords))


@lru_cache()
def stemmize_stopwords():
    return list(set([
        stemmize(stopword)
        for stopword in default_stopwords()
    ]))
