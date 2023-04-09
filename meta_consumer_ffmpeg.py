import json
import subprocess
from pathlib import Path

BASE_DIR = Path().cwd()
MEDIA_DIR = str(BASE_DIR)+r'\media_assets\47714c03-e170-4d4a-9e24-6be15bf53e6f.mp4'
print(MEDIA_DIR)

# Load the JSON data
with open('meta_dict.json') as f:
    data = json.load(f)

# Extract the file paths of the media assets in order
file_paths = []
for key in sorted(data.keys()):
    # print("DEBUG",data[key])
    file_paths.append(data[key]['MEDIA_ASSET']['file_path'])

formatted_file_paths=[str(BASE_DIR)+"\\"+x for x in file_paths]
# print(formatted_file_paths)

cmd = r"""ffmpeg -i media_assets\\47714c03-e170-4d4a-9e24-6be15bf53e6f.mp4 -i media_assets\\fbf1ca1e-4051-428a-8e65-12458e448b63.mp4 -filter_complex "[0:v]scale=1920x1080,setsar=1[v0];[1:v]scale=1920x1080,setsar=1[v1];[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -c:a aac -strict -2 output.mp4"""

path_cmd = ""
for path in file_paths:
    path_cmd += f"-i {path} "

cmd = rf"""ffmpeg -y {path_cmd} -filter_complex "[0:v]scale=1920x1080,setsar=1[v0];[1:v]scale=1920x1080,setsar=1[v1];[v0][v1]concat=n=2:v=1[v]" -map "[v]" -c:v libx264 -strict -2 output.mp4"""
subprocess.call(cmd)

#TODO
# clip video as per the length
# join video #
# join audio 
# overlap video + audio 