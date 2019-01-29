# -*- coding: utf-8 -*-
from underthesea import word_tokenize, pos_tag, chunk, ner, sentiment
from underthesea.classification import classify
import click


class Example:
    def __init__(self):
        pass

    def word_segment(self, words):
        results = word_tokenize(words, format="text")
        print(results)

    def pos_tagging(self, words):
        results = pos_tag('Chợ thịt chó nổi tiếng ở Sài Gòn bị truy quét')
        print(results)

    def chunking(self, words):
        results = chunk(words)
        print(results)

    def name_entity_recognition(self, words):
        results = ner(words)
        print(results)

    def intent_detection(self, words):
        results = classify(words)
        print(results)

    def sentiment_analysis(self, words):
        results = sentiment(words)
        print(results)

    def sampleFunc(arg):
        print('you called sampleFunc({})'.format(arg))


@click.command()
@click.option('--method', '-m')
@click.option('--sentence', '-s')
def main(method, sentence):
    m = globals()['Example']()
    func = getattr(m, 'sampleFunc')
    func(sentence)


if __name__ == "__main__":
    main()
