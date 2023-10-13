from videoprocessor import audio_process, video_process
from imageprocessor import image_processing
from textprocessor import processText
from pdfprocessor import processpdf
import os

def processdocs(dataset, docpath):
    try:
        docist=docpath.split('.')
        format=docist[1]
        if format == 'wav':
            #its an audio file
            audiotext=audio_process(dataset, docpath)
            print(audiotext)
        elif format=='mp4':
            #its a video file
            videotext=video_process(dataset, docpath)
            print(videotext)
        elif format=='png' or format=='jpg' or format=='jpeg':
            #its an image
            imgtext=image_processing(dataset, docpath)
            print(imgtext)
        elif format=='pdf':
            #its a pdf file
            pdftext=processpdf(dataset, docpath)
            print(pdftext)
        elif format=='txt' or format=='docx' or format=='doc':
            #its a text file
            text=processText(dataset, docpath)
            print(text)
    except Exception as e:
        print(e)


example_doc_list=[f"Workforce/{file}" for file in os.listdir('Workforce')]
print(example_doc_list)
for file in example_doc_list:
    print(f'Starting to process {file}')
    processdocs('Dataset.csv',file)
    print(f'Finished Processing {file}')


