import os
import requests
import json
from dotenv import dotenv_values
config = dotenv_values(".env")

def search_videos(query):
    url = "https://api.pexels.com/videos/search"
    headers = {
        "Authorization": config["PEXELS_API_KEY"]
    }
    params = {
        "query": query,
        "orientation":"landscape",
        "per_page": 10
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("Error: ", response.status_code)
        return None
    data = json.loads(response.text)
    videos = data.get("videos")
    if not videos:
        print("No videos found.")
        return None
    result = []
    for video in videos:
        video_url = video.get("url")
        video_id = video.get("id")
        video_duration = video.get("duration")
        video_image = video.get("image")
        video_user = video.get("user")
        video_size = f'{video.get("width")}X{video.get("width")}'
        video_files = video.get("video_files")
        if not video_files:
            print("No video files found for video ", video_id)
            continue
        # Select the highest resolution video file
        video_file = max(video_files, key=lambda f: f.get("width"))
        video_link = video_file["link"]
        video_data = {
            # "id": video_id,
            # "url": video_url,
            "duration": video_duration,
            # "image": video_image,
            # "user": video_user,
            "size": video_size,
            # "video_file":video_file,
            "link":video_link
        }
        result.append(video_data)
        
    return result

def download_video(url,file_name,folder):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Set the file path based on the URL and folder
    file_name = file_name
    file_path = f"{os.path.join(folder, file_name)}.mp4"
    
    # Download the video
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print("Error: ", response.status_code)
        return None
    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print("DEBUG: Video saved as", file_path)
    return file_path

def search_with_mindura_dwnld(query,min_duration):
    results= search_videos(query)
    if results != None:
        for i,result in enumerate(results):
            # to print duration of all assets
            # print(f"DEBUG: video duration {result['duration'] }")
            if results[i]["duration"] > min_duration:
                op_result= results[i]
                file_path=download_video(result["link"],query,"media_assets")
                op_result["file_path"]=file_path
                op_result["keyword"]=query
                return op_result
    return None

if __name__ == "__main__":
    result=search_with_mindura_dwnld("cats",20)

    