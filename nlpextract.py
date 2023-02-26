import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from collections import defaultdict
from heapq import nlargest

def jz_extract_keywords(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)

    # Identify physical objects using WordNet
    physical_objects = []
    for word in words:
        synsets = wordnet.synsets(word)
        for synset in synsets:
            if synset.pos() == 'n' and synset.lexname() == 'noun.artifact':
                physical_objects.append(word.lower())

    # If at least two physical objects are found, return the top two
    if len(physical_objects) >= 2:
        return physical_objects[:2]

    # Otherwise, fall back to using the extract_keywords() function
    else:
        # print(f"DEBUG: physical_objects: {physical_objects} \n  falling back to keywords algo")
        # Remove stop words and punctuation from the sentence
        stop_words = set(nltk.corpus.stopwords.words('english'))
        words = [word.lower() for word in words if word.lower() not in stop_words and word.isalpha()]

        # Calculate the frequency of each word
        freq = defaultdict(int)
        for word in words:
            freq[word] += 1

        # Calculate the score for each word based on its frequency
        scores = {word: freq[word] for word in freq}

        # Select the top two keywords based on their scores
        keywords = nlargest(2, scores, key=scores.get)
        
        #If at least one physical objects is found, return that one with another kw
        if len(physical_objects) == 1:
            print(f"that one physical object is {physical_objects}")
            if keywords[0] == physical_objects[0]:
                return [physical_objects[0],keywords[1]]
            else:
                return [physical_objects[0],keywords[1]]
        return keywords
    
if __name__ == "__main__":
    # Example usage
    sentence1 = "They still keep their relationship professional at work, but everyone can see the love in their eyes when they look at each other."
    physical_objects1 = jz_extract_keywords(sentence1)
    print(physical_objects1)

