from collections import Counter
import nltk

EXTRA_STOPWORDS = [',', '.', 'srs', 'sr.', 'sra.', 'deputado', 'presidente',
                   'é', ':', "''", '`', '!', '``', '?', 'nº', 's.a.']


def stemmize(token, stem_reference=None):
    token = token.casefold()
    stemmer = nltk.stem.RSLPStemmer()
    stemmed = stemmer.stem(token)

    if stem_reference is not None:
        reference = stem_reference.get(stemmed, Counter())
        reference.update([token])
        stem_reference[stemmed] = reference

    return stemmed


def tokenize(text):
    return nltk.tokenize.word_tokenize(text, language='portuguese')


def stemmize_stopwords(stopwords=None):
    default_stopwords = nltk.corpus.stopwords.words('portuguese')
    if stopwords is not None:
        default_stopwords += stopwords

    return list(set([
        stemmize(stopword)
        for stopword in default_stopwords
    ]))


def bow(text, method='frequency'):
    tokens = tokenize(text)
    stopwords = stemmize_stopwords(stopwords=EXTRA_STOPWORDS)
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
