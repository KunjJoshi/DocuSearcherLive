# -*- coding: utf-8 -*-
"""TextProcessor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YLMWbDS8eonkyELcX-fqQzAed2by00l2
"""

import pandas as pd
from textblob import TextBlob
from pdfprocessor import autocorrect

def processText(dataset, textfile):
  df=pd.read_csv(dataset)
  paths=list(df['Path'])
  texts=list(df['Text'])
  pages=list(df['PageNo'])
  frames=list(df['FrameNo'])
  columns=list(df['Column'])
  lines=list(df['LineNo'])
  with open(textfile,'r', encoding='utf-8') as f:
    textdata=f.read()
  textdata=str(textdata)
  textdata=textdata.split('\n')
  for i in range(len(textdata)):
    paths.append(textfile)
    texts.append(textdata[i])
    pages.append(None)
    frames.append(None)
    columns.append(None)
    lines.append(i)
  data={'Path':paths, 'PageNo':pages, 'FrameNo':frames, 'Column':columns, 'LineNo':lines, 'Text':texts}
  df=pd.DataFrame(data)
  df.to_csv(dataset, index=False)
  return df.tail()
  

