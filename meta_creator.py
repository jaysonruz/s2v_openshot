from Keyword_extractor_paid import Keyword_extractor_paid,break_sentences_split
from useful_functions import python_audio_generator
from assets_handler import search_with_mindura_dwnld,fetch_and_download_image
from kwd_scraper import Keyword_extractor_free # <-----------------------------jugad
import json

def meta_Creator(text):
    meta_dict = {}
    sentences = break_sentences_split(text)
    for i,sentence in enumerate(sentences):
        # returns list of 5 keywords
        keywords = Keyword_extractor_free(sentence)
        print(f"DEBUG: KEYWORDS-> {keywords}")
        # return dict containing meta information of tts
        tts_dict=python_audio_generator(sentence,f"speech_{i}")
        
        # fetching appropriate video assets
        asset_dict=None
        for keyword in keywords[:1]:
            asset_dict = search_with_mindura_dwnld(keyword,min_duration=tts_dict['audio_length'])
            if asset_dict is None:
                continue
            else:
                print(f"DEBUG: KEYWORD chosen for video: {keyword}")
                break
        
        # fetching appropriate image assets    
        if asset_dict is None:
            for keyword in keywords:
                asset_dict = fetch_and_download_image(keyword)
                if asset_dict is None:
                    continue
                else:
                    print(f"DEBUG: KEYWORD chosen for image: {keyword}")
                    break 
        meta_dict[i]={"SENTENCE":sentence,"KEYWORDS":keywords,"TTS":tts_dict,"MEDIA_ASSET":asset_dict}
        
    # Save the dictionary as a JSON file in the current directory
    with open("meta_dict.json", "w") as outfile:
        json.dump(meta_dict, outfile)
    return meta_dict

if __name__ == "__main__":
    input_text = """In 2023, farming and agriculture continue to be critical industries for food security and economic growth around the world. However, these industries are facing significant challenges, including climate change, water scarcity, and labor shortages.
To address these challenges, farmers and agricultural organizations are adopting new technologies and practices to increase efficiency and sustainability. For example, precision agriculture uses sensors, drones, and other technologies to optimize crop yields and reduce waste. Vertical farming and hydroponics are also gaining popularity as ways to grow crops in urban areas with limited space and resources.
Sustainability is also a top priority for many farmers and agricultural organizations. They are working to reduce their carbon footprint by using renewable energy sources, reducing waste and pollution, and conserving natural resources.
"""
    meta_json = meta_Creator(input_text)
    print(meta_json)