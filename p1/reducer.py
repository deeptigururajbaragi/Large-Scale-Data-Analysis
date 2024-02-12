#!/usr/bin/python

from sys import stdin

current_word = None
word = None
word_counts = {}  # Use a dictionary to store word counts for each document

for line in stdin:
    # remove leading and trailing whitespace (including newlines)
    line = line.strip()
    # split into word and document name
    word, document = line.split('\t', 1)

    # while the word is the same, keep counting occurrences in each document
    if current_word == word:
        if document in word_counts:
            word_counts[document] += 1
        else:
            word_counts[document] = 1
    else:
        # otherwise, we received a new word, so print the existing word and its counts
        if current_word:
             # Sort the documents by word count and filename 
            sorted_documents = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
            sorted_doc_strings = [f"{word_count}  {doc}" for doc, word_count in sorted_documents]
            print(current_word, ', '.join(sorted_doc_strings))
        current_word = word
        word_counts = {document: 1}

# Display last word and its counts
if current_word == word:
    # Sort the documents by word count and filename
    sorted_documents = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
    sorted_doc_strings = [f"{word_count}  {doc}" for doc, word_count in sorted_documents]
    print(current_word, ', '.join(sorted_doc_strings))
