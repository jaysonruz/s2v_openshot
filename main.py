import Openshot
import urllib.request
from pathlib import Path
# HOME_DIR = Path.cwd()

# instantiating project in openshot
openshot = Openshot.OpenshotProject(project_name="bombay_project")
# media file path
media_file = "/home/jzruz/Downloads/KSHMR Lost Stories - Bombay Dreams [feat. Kavita Seth] (Official Music Video).mp4"

# openshot uploade media + create clips of it
openshot.Upload_clip_to_project(media_file,position=10,start=0,end=40)

# export and get url
export_url = openshot.export()
print(export_url)


urllib.request.urlretrieve(export_url, 'video_output.mp4')

