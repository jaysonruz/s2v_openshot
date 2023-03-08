import json
from Monclip import monClip
from Openshot import OpenshotProject
import urllib.request
from meta_creator import meta_Creator
from meta_consumer import meta_consumer

def Submit(brief):
    meta_json = meta_Creator(brief)
    myclips=[]
    for key,e in meta_json.items():
        clip = monClip(e["SENTENCE"], e["MEDIA_ASSET"]["keyword"], e["TTS"]["audio_file_path"],e["CAPTION_path"], e["MEDIA_ASSET"]["file_path"], e["TTS"]["audio_length"])
        myclips.append(clip)
    export_url = meta_consumer(myclips)
    return export_url

if __name__ == "__main__":
    brief = """Gotham City was once again shrouded in darkness. But, in the shadows lurked a figure, silently watching over the city. He was Batman, the Dark Knight of Gotham. He moved with a quiet grace, ready to pounce on any criminal who dared to disturb the peace. Batman's fearlessness struck fear into the hearts of those who sought to do evil. No one knew the true identity of the Caped Crusader, but everyone knew that they were safe with him around. As dawn broke over the city, Batman retreated to his lair, ready to face another night of fighting crime."""
    brief_breaks = "They met in a crowded cafe. She spilled coffee on his shirt, and he couldn't stop staring at her smile. A year later, they exchanged vows on the same cafe patio, surrounded by the same people who witnessed their awkward first encounter. From that day on ,they both  knew their love was as sweet and simple as the espresso they shared that fateful day."
    brief_keyword_issue = "They met by chance, eyes locking in a crowded cafe. She spilled her coffee, he helped her clean it up. Days turned into nights, and soon they were inseparable. They laughed, cried, loved. He proposed on a rooftop at sunset, and they lived happily ever after."
    Submit(brief_breaks)
