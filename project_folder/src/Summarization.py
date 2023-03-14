from gensim import corpora


# Wrapper for create_corpora_dict and
def create_bow(texts):
    dictionary = create_corpora_dict(texts)

    # Converts to bag of words format
    corpus_bow = create_corpus_bow(texts, dictionary)

    return corpus_bow, dictionary


# Creates a mapping of word ids to frequency count
def create_corpora_dict(texts):
    all_tokens = []

    for text in texts:
        for doc_tokens in text[1]:
            all_tokens.append(doc_tokens)

    return corpora.Dictionary(all_tokens)


# Converts a document into bag-of-words format using corpora dictionary
def create_corpus_bow(texts, dictionary):
    bow_list = []

    for text in texts:
        text_bow = []
        for doc in text[1]:
            bow = dictionary.doc2bow(doc)
            text_bow.append(bow)
        bow_list.append(text_bow)

    return bow_list


# Calculates total weight of a document
def calc_doc_weight(lsi_corpus):
    weights = []
    for paragraph in lsi_corpus:
        doc_weights = []
        for document in paragraph:
            total_weight = 0
            for word_weight in document:
                if word_weight[1] > 0:
                    total_weight += word_weight[1]
            doc_weights.append(total_weight)
        weights.append(doc_weights)

    return weights


# Transforms a bag-of-words representation to correct vector space using provided model
def corpus_transform(corpus_bow, model):
    full_transform = []
    for paragraph in corpus_bow:
        transformed_paragraph = []
        for document in paragraph:
            transformed_doc = model[document]
            transformed_paragraph.append(transformed_doc)
        full_transform.append(transformed_paragraph)

    return full_transform


# Combines each weight in weights with its relevant document in corpus
def combine_weights_corpus(weights, corpus):
    combined = []
    i = 0
    while i < len(corpus):
        tmp = zip(weights[i], corpus[i][1])
        combined.append((corpus[i][0], list(tmp)))
        i += 1

    return combined


# Outputs the summarized text in a readable layout
def output_format(zipped_list):

    for paragraph in zipped_list:
        print('\n' + paragraph[0] + ':')
        i = 0
        tmp_list = []
        while i < (len(paragraph[1])):
            tmp_list.append(paragraph[1][i][1] + '.')
            i += 1
        print(' '.join(tmp_list))


# Formats the output for use with a User Interface
def output_format_gui(zipped_list):

    formatted_string = ''

    for paragraph in zipped_list:
        formatted_string += '\n' + paragraph[0] + ':' + '\n'
        i = 0
        tmp_list = []
        while i < (len(paragraph[1])):
            tmp_list.append(paragraph[1][i][0] + '.')
            i += 1
        formatted_string += ' '.join(tmp_list) + '\n'

    return formatted_string


# Calculates the distance between the top two high frequency words
def get_word_distance(sentence, high_value_words):

    # Flag to indicate when to count words
    distance_state = 0
    distances = []
    count = 0
    for word in sentence:
        if word in high_value_words and distance_state == 1:
            # print('Toggled state, saved distance')
            distance_state = 0
            distances.append(count)
            count = 0
        elif word in high_value_words:
            distance_state = 1
            # print('Toggled state')

        if distance_state == 1:
            count += 1

    # Gets the average distance of all word distances
    avg_distance = sum(distances) / len(distances)

    return avg_distance


# Sorts the paragraphs based on the distances between high value words
def sort_by_word_distance(summarized_list, frequency_dict):

    # Helper function for list sorting
    def sort_helper(element):
        return element[1]

    def second_helper(element):
        return element[2]

    # Sorts dictionary words from highest to lowest based on how often they appear
    sorted_frequency_dict = sorted(frequency_dict.items(), key=sort_helper, reverse=True)[:2]
    high_value_words = []

    distance_sorted_list = []

    # Creates list of high value words
    for word_pair in sorted_frequency_dict:
        high_value_words.append(word_pair[0])

    # Summarizes based on high value words
    for paragraph in summarized_list:
        distance_sorted_paragraph = []
        for sentence in paragraph[1]:
            words = sentence[1].split()
            count = 0
            for word in words:
                if word in high_value_words:
                    count += 1
            if count > 1:
                distance = get_word_distance(words, high_value_words)
                distance_sorted_paragraph.append((sentence[1], sentence[0], distance))

        if distance_sorted_paragraph:
            distance_sorted_list.append((paragraph[0], sorted(distance_sorted_paragraph, key=second_helper)))

    tmp = combined_summarizer(distance_sorted_list)

    return tmp


def combined_summarizer(values_list):
    def sort_helper(element):
        return element[1] + element[2]

    summarized_list = []

    for x in values_list:
        summarized_list.append((x[0], sorted(x[1], key=sort_helper, reverse=True)))

    return summarized_list




