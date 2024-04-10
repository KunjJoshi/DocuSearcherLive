from googlelinkbringer import getGooglePages
import pandas as pd
import webbrowser
import os
import ast
import json
from textsimilarity import calculate_cosine_similarity

def refine_search(search_res):
    curr_dir=os.path.dirname(__file__)
    allpaths=[search['path'] for search in search_res]
    donepaths=[]
    refinedres=[]
    for path in allpaths:
        if path not in donepaths:
            pathindices=[i for i in range(len(allpaths)) if allpaths[i]==path]
            searchdict={}
            searchlist=[]
            searchdict['path']=path
            searchdict['pathhref']='file:///'+os.path.join(curr_dir, path)
            ext=os.path.splitext(os.path.basename(path))[-1]
            for index in pathindices:
                if ext in ['.txt','.doc','.docx']:
                    linedict={}
                    linedict['line']=search_res[index]['lineno']
                    linedict['text']=search_res[index]['text']
                    linedict['similarity']=search_res[index]['similarity']
                    if linedict not in searchlist:
                      searchlist.append(linedict)
                
                if ext in ['.pdf']:
                    pdfdict={}
                    pagenolist=[search_res[i]['pageno'] for i in pathindices]
                    pagenolist=list(set(pagenolist))
                    for pageno in pagenolist:
                        linenums=[{'line':search['lineno'],'text':search['text'], 'similarity':search['similarity']} for search in search_res if search['path']==path and search['pageno']==pageno]
                        cleanednums=[]
                        for num in linenums:
                            if num not in cleanednums:
                                cleanednums.append(num)
                        pdfdict[f'pageno{pageno}']=cleanednums
                    if pdfdict not in searchlist:
                      searchlist.append(pdfdict)
                
                if ext in ['.aud', '.mp3', '.mp4', '.wav']:
                    movdict={}
                    movdict['frame']=search_res[index]['frameno']
                    movdict['text']=search_res[index]['text']
                    movdict['similarity']=search_res[index]['similarity']
                    if movdict not in searchlist:
                      searchlist.append(movdict)
                
                if ext in ['.xlsx','.xls','.csv']:
                    tabdict={}
                    cols=[search_res[i]['column'] for i in pathindices]
                    cols=list(set(cols))
                    for col in cols:
                        rows=[{'row':search['row'], 'text':search['text'], 'similarity':search['similarity']} for search in search_res if search['path']==path and search['column']==col]
                        cleanedrows=[]
                        for row in rows:
                            cleanedrows.append(row)
                        tabdict[col]=cleanedrows
                    if tabdict not in searchlist:
                      searchlist.append(tabdict)
            searchdict['search']=searchlist
            refinedres.append(searchdict)
            donepaths.append(path)
        else:
            continue
    return refinedres

def search(search_term):
    curr_dir=os.path.dirname(__file__)
    i=0
    search_results=[]
    df=pd.read_csv('Dataset.csv')
    allpaths=df['Path']
    alltexts=df['Text']
    pages=df['PageNo']
    frames=df['FrameNo']
    lines=df['LineNo']
    columns=df['Column']
    for j in range(len(alltexts)):
        if os.path.splitext(os.path.basename(allpaths[j]))[-1] in ['.csv','.xls','.xlsx']:
            #print(alltexts[j])
            try:
              textdict=ast.literal_eval(alltexts[j])
              textkeys=list(textdict.keys())
              for key in textkeys:
                  value=textdict[key]
                  if search_term.strip().lower() in str(value).strip().lower() or search_term.strip().lower()==str(value).strip().lower() or str(value).strip().lower() in search_term.strip().lower():
                          i=i+1
                          searchdict={}
                          searchdict['result']=i
                          searchdict['path']=allpaths[j]
                          searchdict['pathhref']='file:///'+os.path.join(curr_dir, allpaths[j])
                          searchdict['column']=columns[j]
                          searchdict['row']=key
                          searchdict['text']=textdict[key]
                          sim=calculate_cosine_similarity(searchdict['text'], search_term)
                          searchdict['similarity']=sim
                          print(sim)
                          if sim>0.55:
                               search_results.append(searchdict)
            except:
                continue
        else:
              if search_term.strip().lower() in str(alltexts[j]).strip().lower() or search_term.strip().lower() == str(alltexts[j]).strip().lower() or str(alltexts[j]).strip().lower() in search_term.strip().lower() :
                  i=i+1
                  searchdict={}
                  searchdict['result']=i
                  searchdict['path']=allpaths[j]
                  searchdict['pathhref']='file:///'+os.path.join(curr_dir, allpaths[j])
                  extension=os.path.splitext(os.path.basename(allpaths[j]))[-1]
                  if extension in ['.txt','.doc','.docx']:
                      resline=lines[j]
                      searchdict['lineno']=resline
                      searchdict['text']=alltexts[j]
                      sim=calculate_cosine_similarity(searchdict['text'], search_term)
                      searchdict['similarity']=sim
                      if sim>0.5:
                            search_results.append(searchdict)
                
                  if extension in ['.pdf']:
                      respage=pages[j]
                      resline=lines[j]
                      searchdict['pageno']=respage
                      searchdict['lineno']=resline
                      searchdict['text']=alltexts[j]
                      sim=calculate_cosine_similarity(searchdict['text'], search_term)
                      searchdict['similarity']=sim
                      if sim>0.5:
                            search_results.append(searchdict)
                
                  if extension in ['.mp4','.mp3','.aud','.wav']:
                      resframe=frames[j]
                      searchdict['frameno']=resframe
                      searchdict['text']=alltexts[j]
                      sim=calculate_cosine_similarity(searchdict['text'], search_term)
                      searchdict['similarity']=sim
                      if sim>0.5:
                            search_results.append(searchdict)
    search_results=refine_search(search_results)
    links=getGooglePages(search_term)
    #links=[]
    dicoflinks=[]
    for link in links:
        if len(link.split('.'))>=2:
           linker=link.split('.')[1]
        else:
            linker=link
        linkdict={}
        linkdict['name']=linker
        linkdict['href']=link
        dicoflinks.append(linkdict)
    output={}
    output['term']=search_term
    output['search']=search_results
    output['google']=dicoflinks
    output_file=f"searchjson/{search_term}Results.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=5)


input_term=input('Enter Input Term: ')
search(input_term)



