from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from collections import defaultdict
import re


# Extracts sentences and associated font sizes from pdf document
# Borrowed from https://stackoverflow.com/questions/68097779/how-to-find-the-font-size-of-every-paragraph-of-pdf-file-using-python-code
def extract_text_with_font_sizes(data):

    path = data

    extracted_data = []

    for page_layout in extract_pages(path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            font_size = round(character.size, 0)
                extracted_data.append((font_size, (element.get_text())))

    return extracted_data


# Iterates through extracted data and creates list of unique text sizes
def get_text_sizes(data):
    font_sizes = []

    for pair in data:
        rounded_size = round(pair[0], 2)
        if rounded_size not in font_sizes:
            font_sizes.append(rounded_size)

    return font_sizes


def get_common_sizes(data):

    def sort_helper(element):
        return element[1]

    font_size_count = defaultdict(int)

    for pair in data:
        rounded_size = round(pair[0], 2)
        font_size_count[rounded_size] += 1

    return sorted(font_size_count.items(), key=sort_helper)


# Iterates through text and extracts potential headings based on font size
def get_headings(text, heading_size):
    headings = []
    for pair in text:
        if pair[0] == heading_size:
            headings.append(pair[1])

    return headings


# Iterate through text and extracts potential paragraph bodies associated with specific headings
def get_body(text, text_size, heading_size):
    paragraphs = []
    paragraph = []
    for pair in text:
        if pair[0] == text_size:
            sentences = re.split(r'(?<!\w\.\w)[.?!]\s', pair[1])
            paragraph.extend(sentences)
        elif pair[0] == heading_size:
            paragraphs.append(paragraph)
            paragraph = []
        else:
            pass
    paragraphs.pop(0)
    paragraphs.append(paragraph)
    return paragraphs


# Combines headings and bodys into one list
def combine_list(headings, bodys):
    i = 0
    combined_list = []
    while i < len(headings):
        combined_list.append((headings[i], bodys[i]))
        i += 1

    return combined_list


# Removes new line characters and PDF formatting artifacts from the text
def clean_data(data):
    cleaned = []

    # Removes new line characters
    for pair in data:
        heading = pair[0].replace("\n", "")
        body = []
        for sentence in pair[1]:
            sentence = sentence.replace("\n", "")
            sentence = re.sub('(\\u202f)|(\\x0c)|(•)', '', sentence)
            if sentence != ' ':
                body.append(sentence)

        cleaned.append((heading, body))

    return cleaned


# Wrapper function for all input processing functions
def read_paragraphs(file_name):

    text = extract_text_with_font_sizes(file_name)

    sizes = get_text_sizes(text)

    size_count = get_common_sizes(text)

    sorted_sizes = sorted(sizes)

    body_size = sorted_sizes.index(size_count[len(size_count) - 1][0])

    heading_size = (body_size + 1)

    headings = get_headings(text, sorted_sizes[heading_size])

    paragraphs = get_body(text, sorted_sizes[body_size], sorted_sizes[heading_size])

    parsed_text = combine_list(headings, paragraphs)

    return parsed_text
