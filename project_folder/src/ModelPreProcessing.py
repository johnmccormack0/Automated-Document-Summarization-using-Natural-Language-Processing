from nltk.corpus import stopwords
from collections import defaultdict


# Splits the document in the Corpus into tokens
def tokenize(corpus):
    complete_token_list = []

    for paragraph in corpus:
        paragraph_tokens = []
        for document in paragraph[1]:
            tokens = document.split(' ')
            tokens = remove_stopwords(tokens)

            paragraph_tokens.append(tokens)

        complete_token_list.append((paragraph[0], paragraph_tokens))

    return complete_token_list


# Removes stop words from the token lists
def remove_stopwords(tokened_words):

    removed = []
    for word in tokened_words:
        if word not in stopwords.words('english') and word != '':
            removed.append(word)

    return removed


# Creates a frequency dictionary for the all tokens
def token_frequency(tokens):
    token_frequency_dict = defaultdict(int)

    for token_list in tokens:
        for sentence in token_list[1]:
            for token in sentence:
                token_frequency_dict[token] += 1

    return token_frequency_dict


# Creates a list of tokens that appear more than once
def more_than_once(tokens, frequency_dict):
    correct_pairs = []

    for token_pair in tokens:
        correct_tokens = []
        for document in token_pair[1]:
            doc_tokens = []
            for token in document:
                if frequency_dict[token] > 1:
                    doc_tokens.append(token)
            if doc_tokens:
                correct_tokens.append(doc_tokens)

        correct_pairs.append((token_pair[0], correct_tokens))

    return correct_pairs


