from mutagen.mp3 import MP3

def get_mp3_length(filename):
    audio = MP3(filename)
    length_sec = audio.info.length
    return length_sec


if __name__ == "__main__":
    filename = "speech_2.mp3"
    length_sec = get_mp3_length(filename)
    print(f"The length of {filename} is {length_sec} seconds.")
