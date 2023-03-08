import requests
import urllib.parse
from dotenv import dotenv_values
config = dotenv_values(".env")
import spacy
import json

def break_sentences_nlp(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

def break_sentences_split(text):
    sentences = text.split('.')
    # remove any empty sentences and re-add periods to each sentence
    sentences = [s.strip() + '.' for s in sentences if s.strip()]
    return sentences


def Keyword_extractor_paid(query):
    """
    Extracts keywords from the given query using a paid keyword extraction API.

    Args:
        query (str): A string containing the text to extract keywords from.

    Returns:
        A Lsit of extracted keywords 

    Raises:
        None.
    """
    
    url = "https://textanalysis-keyword-extraction-v1.p.rapidapi.com/keyword-extractor-text"
    text = urllib.parse.quote(query)
    payload = f"wordnum=5&text={text}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": config["KEYWORD_EXTRACTOR_RAPID_API_KEY"],
        "X-RapidAPI-Host": config["KEYWORD_EXTRACTOR_RAPID_API_HOST"]
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    # response = {"keywords":["crowded cafe","cafe","met","crowded","rooftop at sunset"]}
    data = json.loads(response.text)
    return data['keywords']

    
if __name__ == "__main__":
    pass
    text = """They laughed cried loved 
    He proposed on a rooftop at sunset, and they lived happily ever after."""
    response=Keyword_extractor_paid(text)
    sentences = break_sentences_nlp(text)
    print(sentences)
    sentences = break_sentences_split(text)
    print(sentences)
    print(response)

    