import string
import collections
def file_to_words(filename):
    """Read a file and return a sequence of (word, occurances) values.
    """
    print(filename)
    STOP_WORDS = set([
            'a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if', 'in', 
            'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the', 'to', 'with',
            ])
    TR = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    output = []
    with open(filename, 'rt',encoding='iso-8859-1') as f:
        for line in f:
            if line.lstrip().startswith('..'): # Skip rst comment lines
                continue
            line = line.translate(TR) # Strip punctuation
            for word in line.split():
                word = word.lower()
                if word.isalpha() and word not in STOP_WORDS:
                    output.append( (word, 1) )
    return output
def count_words(item):
    # print(item)
    """Convert the partitioned data for a word to a
    tuple containing the word and the number of occurances.
    """
    word, occurances = item
    return (word, sum(occurances))
def partition( mapped_values):
    partitioned_data = collections.defaultdict(list)
    for key, value in mapped_values:
        partitioned_data[key].append(value)
    return list(partitioned_data.items())
