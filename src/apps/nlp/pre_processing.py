from collections import Counter
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
    stopwords = stemmize_stopwords(
        stopwords=[',', '.', 'sr.', 'deputado', 'presidente']
    )
    stem_reference = {}

    text_bow = Counter([
        stemmize(token) for token in tokens
        if stemmize(token, stem_reference=stem_reference) not in stopwords
    ])
    return text_bow, stem_reference
