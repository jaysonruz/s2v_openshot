
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

brief = "This all encompassing experience wore off for a moment and in that moment, my awareness came gasping to the surface of the hallucination "
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
# print("DEBUG: tss_meta_list: ",meta_list)
myclips = []
for e in meta_list:
    asset_file = search_with_mindura_dwnld(e["keyword1"],min_duration=10)
    if asset_file is None:
        asset_file = search_with_mindura_dwnld(e["keyword2"],min_duration=10)
    if asset_file is None:
        raise Exception("DEBUG : no video found for both keywords!")
    e["asset"]=asset_file
    print(f"DEBUG: META --> {e} \n")
   
    clip = monClip(e["sentence"], e["asset"]["keyword"], e["audio_file_path"], e["asset"]["file_path"], e["audio_length"])
    myclips.append(clip)

# instantiating project in openshot
openshot = OpenshotProject(project_name="hallucination2")
position=0.0
for clip in myclips:
    print(position)
    print(clip.sentence,"\n")
    # openshot uploade media + create clips of it
    openshot.Upload_clip_to_project(clip.asset,position=position,start=clip.start,end=clip.end,layer=2)
    # openshot uploade audio  + create clips of it
    openshot.Upload_clip_to_project(clip.tts,position=position,start=clip.start,end=clip.end,layer=1)
    position+=clip.duration
    position+=0.2 # buffer
    
# export and get url
export_url = openshot.export()
print(export_url)

# download video from url
urllib.request.urlretrieve(export_url, 'video_output.mp4')
    
