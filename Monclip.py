class monClip:
  """_summary_
  """
  def __init__(self,sentence,keyword,tts_path,caption_path,asset_path,duration):
    self.sentence = sentence
    self.keyword = keyword
    self.tts = tts_path
    self.caption = caption_path
    self.asset = asset_path
    self.duration = duration
    self.start = 0.0
    self.end = self.duration






