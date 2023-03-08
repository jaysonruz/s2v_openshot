import os
import requests
import json
from dotenv import dotenv_values
import uuid
config = dotenv_values(".env")

def fetch_landscape_image(query):
    # Set up the API request URL
    url = f'https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape'

    # Set up the API request headers with your API key
    headers = {
        "Authorization": config["PEXELS_API_KEY"]
    }
    # Send the API request and parse the JSON response
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    # Extract the image URL from the response data and return it
    if 'photos' in data and len(data['photos']) > 0:
        return data['photos'][0]['src']['landscape']
    else:
        return None

def download_image(url,folder):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    # download the image from the URL and save it to the image_asset folder
    unique_filename = str(uuid.uuid4())
    # Set the file path based on the URL and folder
    response = requests.get(url)
    path = f"{os.path.join(folder, unique_filename)}.jpeg"
    with open(path, 'wb') as f:
        f.write(response.content)
    return path

def fetch_and_download_image(query):
    url = fetch_landscape_image(query)
    if url != None:
        file_path=download_image(url,"media_assets")
        result = {'link': url,
        'file_path': file_path ,
        'keyword': query}
        return result
    else:
        return None

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

def download_video(url,folder):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    unique_filename = str(uuid.uuid4())
    # Set the file path based on the URL and folder
    file_path = f"{os.path.join(folder, unique_filename)}.mp4"
    
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
                file_path=download_video(result["link"],"media_assets")
                op_result["file_path"]=file_path
                op_result["keyword"]=query
                return op_result
    return None

if __name__ == "__main__":
    result=search_with_mindura_dwnld("start slipping slowly",1)
    print(result)
    # photos=fetch_and_download_image("start slipping slowly")
    # print(photos)
    
    