
import os
import pyttsx3
import time
import spacy
import pytextrank
import pandas as pd
import urllib.request
from assets_handler import search_with_mindura_dwnld
from useful_functions import keyword_extractor,python_audio_generator
from Monclip import monClip
from Openshot import OpenshotProject
import time
# from nlp_keyword_extractor import nlp_keyword_extractor
# Your code here
def Submit(brief):
    output_of_keyword_extractor=keyword_extractor(brief)
    # print("DEBUG: keywords: ",output_of_keyword_extractor)
    meta_list=[]
    for i,l in enumerate(output_of_keyword_extractor):
        sentence=l["sentence"]
        keyword1 = l["keyword1"]
        keyword2 = l["keyword2"]      
        tts_dict=python_audio_generator(sentence,f"speech_{i}")
        tts_dict['keyword1']=keyword1
        tts_dict['keyword2']=keyword2
        tts_dict['sentence']=sentence
        meta_list.append(tts_dict)
    print("DEBUG: tss_meta_list: ",meta_list)
    myclips = []
    for e in meta_list:
        asset_file = search_with_mindura_dwnld(e["keyword1"],min_duration=e['audio_length'])
        if asset_file is None:
            asset_file = search_with_mindura_dwnld(e["keyword2"],min_duration=e['audio_length'])
        if asset_file is None:
            asset_file = search_with_mindura_dwnld(e["sentence"],min_duration=e['audio_length'])
        if asset_file is None:
            raise Exception(f"DEBUG : no video found for both keywords! and sentence --> {e['keyword1']},{e['keyword2']}, :: {e['sentence']}")
        e["asset"]=asset_file
        print(f"DEBUG: META --> {e} \n")
    
        clip = monClip(e["sentence"], e["asset"]["keyword"], e["audio_file_path"], e["asset"]["file_path"], e["audio_length"])
        myclips.append(clip)
    start_time = time.time()
    # instantiating project in openshot
    print("DEBUG: instantiating project!") 
    openshot = OpenshotProject(project_name="dark Knight rises")

    print("DEBUG: uploading files and creating clips!") 
    position=0.0
    for clip in myclips:
        print(position)
        print(clip.sentence,"\n\n")
        # openshot uploade media + create clips of it
        openshot.Upload_clip_to_project(clip.asset,position=position,start=clip.start,end=clip.end,layer=2)
        # openshot uploade audio  + create clips of it
        openshot.Upload_clip_to_project(clip.tts,position=position,start=clip.start,end=clip.end,layer=1)
        position+=clip.duration
        # position+=0.1 # buffer

    print("DEBUG: Beginning with export of project!")    
    # export and get url
    export_url = openshot.export()
    print(export_url)

    # download video from url
    urllib.request.urlretrieve(export_url, 'video_output.mp4')
    end_time = time.time()

    total_time = end_time - start_time

    print("Execution time: {:.2f} seconds".format(total_time))
    return export_url  
    # return "http://3.7.77.20/media/video/output/49/output-49-33-74ffd716.mp4"

if __name__ == "__main__":
    brief = """Gotham City was once again shrouded in darkness. But, in the shadows lurked a figure, silently watching over the city. He was Batman, the Dark Knight of Gotham. He moved with a quiet grace, ready to pounce on any criminal who dared to disturb the peace. Batman's fearlessness struck fear into the hearts of those who sought to do evil. No one knew the true identity of the Caped Crusader, but everyone knew that they were safe with him around. As dawn broke over the city, Batman retreated to his lair, ready to face another night of fighting crime."""
    brief_breaks = "They met in a crowded cafe. She spilled coffee on his shirt, and he couldn't stop staring at her smile. A year later, they exchanged vows on the same cafe patio, surrounded by the same people who witnessed their awkward first encounter. From that day on ,they both  knew their love was as sweet and simple as the espresso they shared that fateful day."
    brief_keyword_issue = "They met by chance, eyes locking in a crowded cafe. She spilled her coffee, he helped her clean it up. Days turned into nights, and soon they were inseparable. They laughed, cried, loved. He proposed on a rooftop at sunset, and they lived happily ever after."
    Submit(brief_breaks)
