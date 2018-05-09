from collections import Counter
from functools import lru_cache
from nltk.corpus import floresta
from string import digits
import nltk


def stemmize(token, stem_reference=None):
    token = token.casefold()
    stemmer = nltk.stem.RSLPStemmer()
    stemmed = stemmer.stem(token)

    if stem_reference is not None:
        reference = stem_reference.get(stemmed, Counter())
        reference.update([token])
        stem_reference[stemmed] = reference

    return stemmed


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
                  'ficar', 'v.exa.', 'conclusao', ')', '(']

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


def remove_numeric_characters(text):
    remove_digits = str.maketrans('', '', digits)
    return text.translate(remove_digits)


def tokenize(text):
    return nltk.tokenize.word_tokenize(text, language='portuguese')


@lru_cache()
def bow(text, method='frequency'):
    text = remove_numeric_characters(text)
    tokens = tokenize(text)
    stopwords = stemmize_stopwords()
    stem_reference = {}

    text_bow = Counter([
        stemmize(token) for token in tokens
        if stemmize(token, stem_reference=stem_reference) not in stopwords
    ])
    return text_bow, stem_reference


def most_common_words(text, n=None):
    text_bow, reference = bow(text)
    most_common = []

    for token in text_bow.most_common(n):
        stem, frequency = token

        # reference[stem] is a Counter and most_comon(1) return a list
        # of tuples: ('word', occurrences)
        word = reference[stem].most_common(1)[0][0]
        most_common.append((word, frequency))
    return most_common
