from InputProcessing import read_paragraphs, clean_data
from ModelPreProcessing import token_frequency, tokenize, more_than_once
from Summarization import calc_doc_weight, corpus_transform, combine_weights_corpus, create_bow, sort_by_word_distance
from gensim import models
import time


def summarize_wrapper(data):
    return main(data)


def main(data):
    data = read_paragraphs(data)

    corpus = clean_data(data)

    # corpus = index_extraction_wrapper(data)

    tokens = tokenize(corpus)

    # Creates dictionary with frequency of terms
    frequency_dict = token_frequency(tokens)

    # Creates list with words that appear more than once
    texts = more_than_once(tokens, frequency_dict)

    # Converts to bag of words format, Converts list into corpus dictionary
    corpus_bow, dictionary = create_bow(texts)

    # Loads existing models
    # TFIDF model is providing better results at two documents
    lsi_model = models.TfidfModel.load("models/testTfidfModel.model")

    corpus_lsi = corpus_transform(corpus_bow, lsi_model)

    weights_list = calc_doc_weight(corpus_lsi)

    weight_sentence_list = combine_weights_corpus(weights_list, corpus)

    distance_sorted_paragraphs = sort_by_word_distance(weight_sentence_list, frequency_dict)

    return distance_sorted_paragraphs


if __name__ == '__main__':
    main('Considering-Cloud-Services-December-2015_govdoc5.pdf')
    # main('Canada SCC_Data_Gov_Roadmap_EN.pdf')
    # main('Felizardo-Carver2020_Chapter_AutomatingSystematicLiterature (1).pdf')
    # main('ISO-IECJTC1-SC42_N669_Final_Draft_of_ISOIEC_TR_24030__AI_Use_Cases.pdf')
    # main('TSPH_FifthEdition_11_16_2015.pdf')
    # main('100048_b5c2ffc0-6039-4037-9766-c68e579f7ec3_govdoc1.pdf')
    # main('Considering-Cloud-Services-December-2015_govdoc5.pdf')
