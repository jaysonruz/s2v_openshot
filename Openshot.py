import os

import urllib.request
import time
from requests import get, post
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from dotenv import dotenv_values
config = dotenv_values(".env")


class OpenshotProject:
  """_summary_
  """
  def __init__(self,project_name="default_name"):
    self.CLOUD_URL = config['CLOUD_URL']
    self.CLOUD_AUTH = HTTPBasicAuth(config['CLOUD_AUTH_USER'],config['CLOUD_AUTH_PWD'])
    # print(config)

    ########################################################
    # Create new project
    end_point = '/projects/'
    project_data = {
        "name": project_name,
        "width": 1920,
        "height": 1080,
        "fps_num": 30,
        "fps_den": 1,
        "sample_rate": 44100,
        "channels": 2,
        "channel_layout": 3,
        "json": "{}",
    }
    r = post(self.CLOUD_URL + end_point, data=project_data, auth=self.CLOUD_AUTH)
    # print(r.json())
    self.project_id = r.json().get("id")
    self.project_url = r.json().get("url")
    print(f"DEBUG: project_id: {self.project_id}\t oproject_url: {self.project_url}")

  def Upload_clip_to_project(self,file_path,position=0.0,start=0.0,end=30.0,layer=1):
    ##########################################################
      # Upload file to project
      end_point = '/projects/%s/files/' % self.project_id
      source_path = file_path
      source_name = os.path.split(source_path)[1]
      file_data = {
          "media": None,
          "project": self.project_url,
          "json": "{}"
      }
      r = post(self.CLOUD_URL + end_point, data=file_data, \
               files={"media": (source_name, open(source_path, "rb"))}, auth=self.CLOUD_AUTH)
      file_url = r.json().get("url")
      print(f"DEBUG: file_url: {file_url}")
      # print(r.json())
    ##########################################################
      # Create a clip for the previously uploaded file
      end_point = '/projects/%s/clips/' % self.project_id
      clip_data = {
          "file": file_url,
          "position": position,
          "start": start,
          "end": end,
          "layer": layer,
          "project": self.project_url,
          "json": "{}"
      }
      r = post(self.CLOUD_URL + end_point, data=clip_data, auth=self.CLOUD_AUTH)
      # print(r.json())
  
  def export(self):
    ##########################################################
      # Create export for final rendered video
      end_point = '/projects/%s/exports/' % self.project_id
      export_data = {
          "video_format": "mp4",
          "video_codec": "libx264",
          "video_bitrate": 8000000,
          "audio_codec": "ac3",
          "audio_bitrate": 1920000,
          "start_frame": 1,
          "end_frame": None,
          "project": self.project_url,
          "json": "{}"
      }
      r = post(self.CLOUD_URL + end_point, data=export_data, auth=self.CLOUD_AUTH)
      export_url = r.json().get("url")
      # print(r.json())
      # return export_url
    ##########################################################
      # Wait for Export to finish (give up after around 40 minutes)
      export_output_url = None
      is_exported = False
      countdown = 500
      while not is_exported and countdown > 1:
          r = get(export_url, auth=self.CLOUD_AUTH)
          print(r.json())
          is_exported = float(r.json().get("progress", 0.0)) == 100.0
          countdown -= 1
          time.sleep(5.0)

      # Get final rendered url
      r = get(export_url, auth=self.CLOUD_AUTH)
      export_output_url = r.json().get("output")
      
      # print(r.json())
      print("Export Successfully Completed: %s!" % export_output_url)
      return export_output_url
  
  
if __name__ =="__main__":
  # instantiating project in openshot
  openshot = OpenshotProject(project_name="bombay1_project")

  # media file path
  media_file = r'media_assets\\the race.mp4'

  # openshot uploade media + create clips of it
  openshot.Upload_clip_to_project(media_file,position=10,start=0,end=40)

  # export and get url
  export_url = openshot.export()
  print(export_url)

  # download video from url
  urllib.request.urlretrieve(export_url, 'video_output.mp4')