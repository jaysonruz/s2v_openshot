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
    input_text = """She'd take the world off my shoulders
If it was ever hard to move.
She'd turn the rain to a rainbow
When I was living in the blue.
Why then, if she is so perfect
Do I still wish that it was you?.
Perfect don't mean that it's working
So what can I do? (Ooh).
When you're out of sight
In my mind.
'Cause sometimes I look in her eyes
And that's where I find a glimpse of us.
And I try to fall for her touch
But I'm thinking of the way it was.
Said I'm fine and said I moved on
I'm only here passing time in her arms.
Hoping I'll find
A glimpse of us
Tell me he savors your glory.
Does he laugh the way I did?
Is this a part of your story?
One that I had never lived.
Maybe one day you'll feel lonely
And in his eyes, you'll get a glimpse.
Maybe you'll start slipping slowly
And find me again
When you're out of sight.
In my mind
'Cause sometimes I look in her eyes.
And that's where I find a glimpse of us
And I try to fall for her touch
But I'm thinking of the way it was.
Said I'm fine and said I moved on
I'm only here passing time in her arms
Hoping I'll find.
A glimpse of us
Ooh, ooh-ooh
Ooh, ooh-ooh
Ooh, ooh, ooh
'Cause sometimes I look in her eyes
And that's where I find a glimpse of us.
And I try to fall for her touch
But I'm thinking of the way it was
Said I'm fine and said I moved on.
I'm only here passing time in her arms
Hoping I'll find
A glimpse of us."""
    meta_json = meta_Creator(input_text)
    print(meta_json)