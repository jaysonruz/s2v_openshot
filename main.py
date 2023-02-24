import Openshot
import urllib.request
from pathlib import Path
# HOME_DIR = Path.cwd()




# instantiating project in openshot
openshot = Openshot.OpenshotProject(project_name="bombay1_project")

# media file path
media_file = r"E:\LearningResource\[FreeCoursesOnline.Me] TalkPython - Getting started with pytest\lesson1.mp4"

# openshot uploade media + create clips of it
openshot.Upload_clip_to_project(media_file,position=10,start=0,end=40)

# export and get url
export_url = openshot.export()
print(export_url)

# download video from url
urllib.request.urlretrieve(export_url, 'video_output.mp4')

