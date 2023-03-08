import json
from Monclip import monClip
from Openshot import OpenshotProject
import urllib.request

def meta_consumer(myclips):
    # instantiating project in openshot
    print("DEBUG: -------instantiating OPENSHOT project!------") 
    openshot = OpenshotProject(project_name="dark Knight rises")

    print("DEBUG: -------uploading files and creating clips!-------") 
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

    print("DEBUG:------- Rendering  project!-------")    
    # export and get url
    export_url = openshot.export()
    print(export_url)

    # download video from url
    urllib.request.urlretrieve(export_url, 'video_output.mp4')
    return export_url  

if __name__ == "__main__":
         # open the file in read mode
    with open('meta_dict.json', 'r') as f:
        data = f.read()
    json_data = json.loads(data)
    myclips=[]
    for key,e in json_data.items():
        clip = monClip(e["SENTENCE"], e["MEDIA_ASSET"]["keyword"], e["TTS"]["audio_file_path"], e["MEDIA_ASSET"]["file_path"], e["TTS"]["audio_length"])
        myclips.append(clip)
    export_url = meta_consumer(myclips)