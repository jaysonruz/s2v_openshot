import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

def identify_physical_objects(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)

    # Identify physical objects using WordNet
    physical_objects = []
    for word in words:
        synsets = wordnet.synsets(word)
        for synset in synsets:
            if synset.pos() == 'n' and synset.lexname() == 'noun.artifact':
                physical_objects.append(word.lower())

    # Remove duplicates and return the list of physical objects
    return list(set(physical_objects))

import spacy

def extract_entities(sentence):
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")
    
    # Process the sentence with the language model
    doc = nlp(sentence)
    
    # Extract physical objects and their attributes
    entities = []
    for token in doc:
        if token.dep_ == "nsubj" and token.pos_ == "NOUN":
            print(" DEBUG:  Found a subject noun ",token.text)
            # Found a subject noun, add it to the entities list
            entity = {"name": token.text, "attributes": []}
            for child in token.children:
                if child.pos_ == "ADJ":
                    # Found an adjective describing the subject, add it to the attributes list
                    entity["attributes"].append(child.text)
            entities.append(entity)
    return entities


# Example usage
sentence = "The table and chair were made of wood"
physical_objects = extract_entities(sentence)
print(physical_objects)

# Example usage
sentence = "The big red apple fell from the tree"
physical_objects = extract_entities(sentence)
print(physical_objects)

sentence = "The red ball rolled under the couch and table and the blue mug fell off the table."
physical_objects = extract_entities(sentence)
print(physical_objects) # Output: ['red ball', 'blue mug']


# python function that identifies physical object and its attributes from a given sentence and returns it 