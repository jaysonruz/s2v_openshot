import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from collections import defaultdict
from heapq import nlargest
from nltk.tokenize import sent_tokenize
from nlpextract import jz_extract_keywords
def split_text(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Filter out short sentences with less than 10 words
    sentences = [s for s in sentences if len(s.split()) >= 5]

    return sentences

def nlp_keyword_extractor(text):
    # text = "They met by chance., eyes locking in a crowded cafe. She spilled her. coffee, he helped her clean it up Days turned into nights, and soon they were inseparable. They laughed, cried, loved. He proposed on a rooftop at sunset, and they lived happily ever after."
    sentences = split_text(text)
    # sentence = "The quick brown fox jumped over the lazy dog"
    klist=[]
    for sentence in sentences: 
        keywords = jz_extract_keywords(sentence)
        kuery={'sentence':sentence,'keyword1':keywords[0],'keyword2':keywords[1]}
        klist.append(kuery)
    return klist

if __name__ == "__main__":
    # import nltk
    # nltk.download('stopwords')
    text = "They met by chance., eyes locking in a crowded cafe. She spilled her. coffee, he helped her clean it up Days turned into nights, and soon they were inseparable. They laughed, cried, loved. He proposed on a rooftop at sunset, and they lived happily ever after."
    kwds=nlp_keyword_extractor(text)
    print(kwds)