from videoprocessor import audio_process, video_process
from imageprocessor import image_processing
from textprocessor import processText
from pdfprocessor import processpdfpagewise
from sheetprocessor import process_sheet
import os

def processdocs(dataset, docpath):
        format=os.path.splitext(os.path.basename(docpath))[-1]
        #print(format)
        if format == '.wav':
            #its an audio file
            audiotext=audio_process(dataset, docpath)
            print(audiotext)
        elif format=='.mp4':
            #its a video file
            videotext=video_process(dataset, docpath)
            print(videotext)
        elif format=='.png' or format=='.jpg' or format=='.jpeg':
            print('its an image')
            imgtext=image_processing(dataset, docpath)
            print(imgtext)
        elif format=='.pdf':
            #its a pdf file
            pdftext=processpdfpagewise(dataset, docpath)
            print(pdftext)
        elif format=='.txt' or format=='.docx' or format=='.doc':
            #its a text file
            text=processText(dataset, docpath)
            print(text)
        elif format=='.csv' or format=='.xls' or format=='.xlsx':
            text=process_sheet(dataset, docpath)
            print(text)


filename='D://Datapit Search/WorkForce/terrorist.txt'
processdocs('Dataset.csv', filename)


