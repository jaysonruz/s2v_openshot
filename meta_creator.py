from Keyword_extractor_paid import Keyword_extractor_paid,break_sentences_split
from useful_functions import python_audio_generator
from assets_handler import search_with_mindura_dwnld,fetch_and_download_image
from kwd_scraper import Keyword_extractor_free # <-----------------------------jugad
import json
from captiongen import create_svg_file
def meta_Creator(text):
    meta_dict = {}
    sentences = break_sentences_split(text)
    for i,sentence in enumerate(sentences):
        # returns list of 5 keywords
        keywords = Keyword_extractor_free(sentence)
        print(f"DEBUG: KEYWORDS-> {keywords}")
        # return dict containing meta information of tts
        tts_dict=python_audio_generator(sentence,f"speech_{i}")
        
        # return dict containing meta information of captions
        caption_svg_file = create_svg_file(sentence)
         
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
        meta_dict[i]={"SENTENCE":sentence,"KEYWORDS":keywords,"TTS":tts_dict,"CAPTION_path":caption_svg_file,"MEDIA_ASSET":asset_dict}
        
    # Save the dictionary as a JSON file in the current directory
    with open("meta_dict.json", "w") as outfile:
        json.dump(meta_dict, outfile)
    return meta_dict

if __name__ == "__main__":
    input_text = """Climate and agriculture are intricately linked, as the weather patterns and temperature fluctuations can greatly impact the success of crops and the livelihoods of farmers.Climate change has led to more extreme weather events, such as droughts, floods, and heatwaves, which can negatively affect agriculture. Changes in precipitation patterns can also cause problems, as farmers need a consistent supply of water for their crops.
hydroponic farming is the new norm."""
    meta_json = meta_Creator(input_text)
    print(meta_json)