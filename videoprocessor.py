# -*- coding: utf-8 -*-
"""VideoProcessor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NzDj9Z_v7FfJOpI5xXIxUhVtwj6rii1y
"""

from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, MarianMTModel, MarianTokenizer
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import torchaudio
import librosa
import torch
import easyocr
import os
import cv2
import pandas as pd
from textblob import TextBlob
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd='/usr/bin/tesseract'
custom_config=r'--oem 3 --psm 6 -l eng'

def convert_mp4_to_images(video_path):
  output_path='outputframes/'
  os.makedirs(output_path, exist_ok=True)
  cap=cv2.VideoCapture(video_path)
  frames=0
  framelist=[]
  while True:
    ret,frame=cap.read()
    if not ret:
      break
    imgname=os.path.join(output_path, f'frameno{frames:04d}.jpg')
    cv2.imwrite(imgname, frame)
    #print(f'Saved Frame No{frames} at {imgname}')
    frames=frames+1
    framelist.append(imgname)
  cap.release()
  print(f"Total Saved Frames: {frames}")
  return framelist

def get_unique_text_list(img_files):
  alltexts=[]
  frameout=[]
  print(len(img_files))
  for i in range(len(img_files)):
    framedict={}
    file=img_files[i]
    img=Image.open(file)
    text=pytesseract.image_to_string(img, config=custom_config)
    corrtext=autocorrect(text)
    if corrtext not in alltexts:
      framedict['frameno']=i
      framedict['text']=corrtext
      alltexts.append(corrtext)
      frameout.append(framedict)
    print(f'Completed frame {i}')
  return frameout


def create_vid_text(utl):
  fintext=''
  for text in utl:
    text=text.lower()
    fintext=fintext+text+' '
  return fintext

def get_mp4_audio(video_path):
  video=VideoFileClip(video_path)
  audio=video.audio
  op_aud='extracted.wav'
  audio.write_audiofile(op_aud)
  video.close()
  return op_aud

def refine_audio(aud_file):
  op_aud='refined.wav'
  audio=AudioSegment.from_file(aud_file)
  audio=audio.set_channels(1).set_sample_width(2).set_frame_rate(16000)
  audio.export(op_aud, format='wav')
  return op_aud

def eng_transcribe(aud_path):
  model_name="jonatasgrosman/wav2vec2-large-xlsr-53-english"
  model=Wav2Vec2ForCTC.from_pretrained(model_name)
  processor=Wav2Vec2Processor.from_pretrained(model_name)
  aud, sr=torchaudio.load(aud_path)
  inputs=processor(aud.squeeze().numpy(), sample_rate=16_000, return_tensors="pt")
  with torch.no_grad():
    logits=model(inputs.input_values, attention_mask=inputs.attention_mask).logits
  predicted_ids=torch.argmax(logits, dim=-1)
  pred_str=processor.decode(predicted_ids[0])
  return pred_str

def autocorrect(text):
  correct_text=TextBlob(text).correct()
  correct_text=str(correct_text)
  return correct_text

def video_process(dataset, video_path):
  df=pd.read_csv(dataset)
  paths=list(df['Path'])
  texts=list(df['Text'])
  frames=list(df['FrameNo'])
  pages=list(df['PageNo'])
  lines=list(df['LineNo'])
  columns=list(df['Column'])
  framelist=convert_mp4_to_images(video_path)
  lot=get_unique_text_list(framelist)
  for frame in lot:
    paths.append(video_path)
    frames.append(frame['frameno'])
    texts.append(frame['text'])
    pages.append(None)
    columns.append(None)
    lines.append(None)
  
  vidaud=get_mp4_audio(video_path)
  refaud=refine_audio(vidaud)
  vidtext=eng_transcribe(refaud)
  corrected_text=autocorrect(vidtext)
  paths.append(video_path)
  texts.append(corrected_text)
  pages.append(None)
  columns.append(None)
  lines.append(None)
  frames.append(None)
  data={'Path':paths, 'PageNo':pages, 'FrameNo':frames, 'LineNo':lines, 'Column':columns, 'Text':texts}
  df=pd.DataFrame(data)
  df.to_csv(dataset, index=False)
  return df.tail()

def audio_process(dataset, audiofile):
  df=pd.read_csv(dataset)
  paths=list(df['Path'])
  texts=list(df['Text'])
  frames=list(df['FrameNo'])
  pages=list(df['PageNo'])
  lines=list(df['LineNo'])
  columns=list(df['Column'])
  refaud=refine_audio(audiofile)
  audtext=eng_transcribe(refaud)
  corrected_text=autocorrect(audtext)
  paths.append(audiofile)
  texts.append(corrected_text)
  pages.append(None)
  columns.append(None)
  lines.append(None)
  frames.append(None)
  data={'Path':paths, 'PageNo':pages, 'FrameNo':frames, 'LineNo':lines, 'Column':columns, 'Text':texts}
  df=pd.DataFrame(data)
  df.to_csv(dataset, index=False)
  return df.tail()
