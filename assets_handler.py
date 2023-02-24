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
        video_data = {
            "id": video_id,
            "url": video_url,
            "duration": video_duration,
            "image": video_image,
            "user": video_user,
            "size": video_size
        }
        result.append(video_data)
    return result

if __name__ == "__main__":
    results= search_videos("Cars")
    for x in results:
     print(f"\n DEBUG: {x}")
    # print(results)