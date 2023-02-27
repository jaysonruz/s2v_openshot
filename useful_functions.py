import os
import pyttsx3
import time
import spacy
import pytextrank
import pandas as pd
from assets_handler import search_with_mindura_dwnld
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
                query={'sentence':s,'keyword1':doc._.phrases[0].text,'keyword2':doc._.phrases[0].text}
                ordered_queries.append(query)

            else:
                query={'sentence':s,'keyword1':s,'keyword2':s}
                ordered_queries.append(query)
        else:  
            for phrase in doc._.phrases:
                container_of_keywords.append(phrase.text)


                if len(container_of_keywords)==2:

                    query={'sentence':s,'keyword1':container_of_keywords[0],'keyword2':container_of_keywords[1]}
                    ordered_queries.append(query)

                    break
                    
    return ordered_queries

def python_audio_generator(sentence, file_name):
    """
    takes sentence and returns its tts audio file in mp3 format in audio directory 
    and returns meta information about the same.

    Args:
        sentence (String): Description of the first argument.
        file_name (String): Description of the second argument.

    Returns:
        meta (Dictionary): meta information of audio file generated
    """
    meta={}
    # Make a folder named 'audio'
    if not os.path.exists("audio"):
        os.mkdir("audio")
    engine = pyttsx3.init()
    engine.save_to_file(sentence, os.path.join("audio", file_name + ".mp3"))
    engine.runAndWait()
    audio_file_path = os.path.join("audio", file_name + ".mp3")
    audio_length = get_audio_length(audio_file_path)
    # creating a meta information dict 
    meta["file_name"]=file_name
    meta["audio_file_path"]=audio_file_path
    meta["audio_length"]=audio_length
    # print(file_name," Audio length in seconds:", audio_length)
    return meta
    
def get_audio_length(file_path):
    # Use a package like pydub to get the audio length
    from pydub import AudioSegment
    audio = AudioSegment.from_file(file_path)
    return round(audio.duration_seconds,2)



if __name__ =="__main__":
    brief = """They laughed cried loved.
 He proposed on a rooftop at sunset, and they lived happily ever after."""
    output_of_keyword_extractor=keyword_extractor(brief)
    print("DEBUG: keywords: ",output_of_keyword_extractor)
    meta_list=[]
    for i,l in enumerate(output_of_keyword_extractor):
        sentence=l["sentence"]
        keyword1 = l["keyword1"]
        keyword2 = l["keyword2"]      
        tts_dict=python_audio_generator(sentence,f"speech_{i}")
        tts_dict['keyword1']=keyword1
        tts_dict['keyword2']=keyword2
        meta_list.append(tts_dict)
    # # print("DEBUG: tss_meta_list: ",meta_list)
    # for e in meta_list:
    #     asset_file = search_with_mindura_dwnld(e["keyword1"],min_duration=10)
    #     if asset_file is None:
    #         asset_file = search_with_mindura_dwnld(e["keyword2"],min_duration=10)
    #     if asset_file is None:
    #         raise Exception("DEBUG : no video found for both keywords!")
    #     e["asset"]=asset_file
    #     print(f"DEBUG: META --> {e} \n")
        # download_video(asset_file["url"],"media_assets")
    # from Monclip import monClip
    
    # clip = monClip(sentence, keyword, tts_path, asset_path, duration, layer)