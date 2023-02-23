import os
import pyttsx3
import time
import spacy
import pytextrank
import pandas as pd
# import deplacy






def keyword_extractor(text):
    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)
    
    big_sentences = [sent.text.strip() for sent in doc.sents]
    

    #deplacy.render(doc)

    seen = set() # keep track of covered words

    Chunks = []
    for sent in doc.sents:
        if len(sent.text.split()) < 15:
            Chunks.append(sent)
        else:
            chunks=[]
        
            heads = [cc for cc in sent.root.children if cc.dep_ == 'conj']

            for head in heads:
                words = [ww for ww in head.subtree]
                for word in words:
                    seen.add(word)
                chunk = (' '.join([ww.text for ww in words]))
                chunks.append( (head.i, chunk) )

            unseen = [ww for ww in sent if ww not in seen]
            chunk = ' '.join([ww.text for ww in unseen])
            chunks.append( (sent.root.i, chunk) )

            chunks = sorted(chunks, key=lambda x: x[0])

            chunks= [c[1] for c in chunks]

            for item in chunks:
                Chunks.append(item)
            Chunks=[str(c).strip() for c in Chunks]

    ordered_queries=[]
    nlp.add_pipe("textrank")
    for s in Chunks:
        s=str(s)
        doc = nlp(s)
        container_of_keywords=[]

        if len(doc._.phrases)<2:
            if len(doc._.phrases)==1:
                query=doc._.phrases[0].text
                ordered_queries.append(query)

            else:
                query=s
                ordered_queries.append(query)
        else:  
            for phrase in doc._.phrases:
                container_of_keywords.append(phrase.text)


                if len(container_of_keywords)==2:

                    query={'sentence':s,'keyword1':container_of_keywords[0],'keyword2':container_of_keywords[1]}
                    ordered_queries.append(query)

                    break
                    
    return ordered_queries

def python_audio_generator(sentence,file_name):
    #Make a folder named 'audio'
    if not os.path.exists("tts_folder"):
        os.mkdir("tts_folder")
    engine = pyttsx3.init()
    engine.save_to_file(sentence, f'tts_folder/{file_name}.mp3')
    engine.runAndWait()
        




if __name__ =="__main__":
    brief = "This all encompassing experience wore off for a moment and in that moment, my awareness came gasping to the surface of the hallucination and I was able to consider momentarily that I had killed myself by taking an outrageous dose of an online drug and this was the most pathetic death experience of all time. They decided to settle the argument with a race. They agreed on a route and started off the race. The rabbit shot ahead and ran briskly for some time. Then seeing that he was far ahead of the tortoise, he thought he'd sit under a tree for some time and relax beforecontinuing the race. "
    output_of_keyword_extractor=keyword_extractor(brief)
    print("DEBUG: keywords: ",output_of_keyword_extractor)
    for i,l in enumerate(output_of_keyword_extractor):
        sentence=l["sentence"]    
        python_audio_generator(sentence,f"speech_{i}")