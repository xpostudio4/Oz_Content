#!/usr/bin/python
import os
from flask import Flask, current_app
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
from models import db, Animal

nltk.data.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nltk_data'))

class FrequencySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('english')+ list(punctuation))

    def _compute_frequencies(self, word_sent):
        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        m = float(max(freq.values()))
        final_freq = freq.copy()
        for w in freq.keys():
            final_freq[w] = freq[w]/m
            if final_freq[w] >= self._max_cut or final_freq[w] <= self._min_cut:
                del final_freq[w]
        return final_freq

    def summarize(self, text, n):
        sents = sent_tokenize(text)
        assert n <= len(sents)
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i, sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking, n)
        return [sents[j] for j in sents_idx]

    def _rank(self, ranking, n):
        return nlargest(n, ranking, key=ranking.get)

if __name__ == '__main__':
    app = Flask(__name__)
    STAGE = os.getenv('FLASK_CONFIGURATION_SETTINGS', 'production')

    if STAGE == 'local':
        #configure local database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ozcontent@127.0.0.1:5432/ozcontent'
        app.debug = True
    else:
        #configuration of production
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ufcofxthphdbga:gaXaZs-830eOTtM8a7YccAqnTX@ec2-107-22-187-89.compute-1.amazonaws.com:5432/de0jhotbsj3mbq'

    db.app = app
    db.init_app(app)
    fs = FrequencySummarizer()
    with app.app_context():
        for animal in Animal.query.all():
            animal.summary = fs.summarize(animal.text, 1).pop()
            db.session.commit()
    print("summary created")
