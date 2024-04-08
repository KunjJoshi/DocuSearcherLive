from googlelinkbringer import getGooglePages
import pandas as pd
import webbrowser
import os
import ast
import json

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
                    if linedict not in searchlist:
                      searchlist.append(linedict)
                
                if ext in ['.pdf']:
                    pdfdict={}
                    pagenolist=[search_res[i]['pageno'] for i in pathindices]
                    pagenolist=list(set(pagenolist))
                    for pageno in pagenolist:
                        linenums=[search['lineno'] for search in search_res if search['path']==path and search['pageno']==pageno]
                        linenums=list(set(linenums))
                        linenums=[{'line':no} for no in linenums]
                        pdfdict[f'pageno{pageno}']=linenums
                    if pdfdict not in searchlist:
                      searchlist.append(pdfdict)
                
                if ext in ['.aud', '.mp3', '.mp4', '.wav']:
                    movdict={}
                    movdict['frame']=search_res[index]['frameno']
                    if movdict not in searchlist:
                      searchlist.append(movdict)
                
                if ext in ['.xlsx','.xls','.csv']:
                    tabdict={}
                    cols=[search_res[i]['column'] for i in pathindices]
                    cols=list(set(cols))
                    for col in cols:
                        rows=[search['row'] for search in search_res if search['path']==path and search['column']==col]
                        rows=list(set(rows))
                        rows=[{'row':row} for row in rows]
                        tabdict[col]=rows
                    if tabdict not in searchlist:
                      searchlist.append(tabdict)
            searchdict['search']=searchlist
            refinedres.append(searchdict)
            donepaths.append(path)
        else:
            continue
    return refinedres

def search(search_term):
    search_terms=search_term.split(' ')
    print(search_terms)
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
                  vallist=value.split(' ')
                  for val in vallist:
                      if any(str(st).lower() in str(val).lower() or str(st).lower()==str(val).lower() for st in search_terms):
                          i=i+1
                          searchdict={}
                          searchdict['result']=i
                          searchdict['path']=allpaths[j]
                          searchdict['pathhref']='file:///'+os.path.join(curr_dir, allpaths[j])
                          searchdict['column']=columns[j]
                          searchdict['row']=key
                          search_results.append(searchdict)
            except:
                continue
        else:
          textlist=str(alltexts[j]).split(' ')
          for t in range(len(textlist)):
              if any(str(st).lower() in str(textlist[t]).lower() or str(st).lower()==str(textlist[t]).lower() for st in search_terms):
                  i=i+1
                  searchdict={}
                  searchdict['result']=i
                  searchdict['path']=allpaths[j]
                  searchdict['pathhref']='file:///'+os.path.join(curr_dir, allpaths[j])
                  extension=os.path.splitext(os.path.basename(allpaths[j]))[-1]
                  if extension in ['.txt','.doc','.docx']:
                      resline=lines[j]
                      searchdict['lineno']=resline
                
                  if extension in ['.pdf']:
                      respage=pages[j]
                      resline=lines[j]
                      searchdict['pageno']=respage
                      searchdict['lineno']=resline
                
                  if extension in ['.mp4','.mp3','.aud','.wav']:
                      resframe=frames[j]
                      searchdict['frameno']=resframe
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
    output['search']=search_results
    output['google']=dicoflinks
    output_file=f"searchjson/{search_term}Results.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=5)


input_term=input('Enter Input Term: ')
search(input_term)



