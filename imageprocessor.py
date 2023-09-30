# -*- coding: utf-8 -*-
"""ImageProcessor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iNdEsEPotNsp8vY5uPC54u4TqkvI7kD-
"""

import easyocr
from PIL import Image
import pandas as pd
from textblob import TextBlob

def get_image_text(image_path):
  reader=easyocr.Reader(['en'], gpu=True)
  text=reader.readtext(image_path)
  fulltext=''
  for t in text:
    t=list(t)
    fulltext=fulltext+t[1].lower()+ ' '
  return fulltext

def autocorrect(txt):
  correct_text=TextBlob(txt).correct()
  correct_text=str(correct_text)
  return correct_text


def image_processing(dataset, image_path):
  df=pd.read_csv(dataset)
  img_text=get_image_text(image_path)
  corrected_text=autocorrect(img_text)
  new_row={'Path':[image_path], 'Text':[corrected_text]}
  row=pd.DataFrame(new_row)
  df=pd.concat([df,row], axis=0)
  df.to_csv(dataset, index=False)
  return corrected_text
