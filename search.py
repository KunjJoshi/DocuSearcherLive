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

def create_card_content(res):
    content=f"""
                <div class="card">
            """
    path=res['path']
    element_list=res['search']
    start=f"""
                    <a href="{res['pathhref']}"class="card-heading"><strong>Path to Result:</strong> {res['path']}</a>
    """
    content=content+'\n'+start
    button_start="""
    <ul class="collapsible-list">
        <button class="collapsible-button" onclick="toggleCollapsible(event)">Toggle List</button>
        <div class="collapsible-content">
                """
    ext=os.path.splitext(os.path.basename(path))[-1]
    content=content+'\n'+button_start
    for element in element_list:
            keys=list(element.keys())
            for key in keys:
                if type(element[key])==list:
                    if ext in ['.pdf']:
                        app=''
                        for value in element[key]:
                            for childkey, childvalue in value.items():
                                app=app+'\t'+str(childkey)+' '+str(childvalue)
                    else:
                        app=''
                        for value in element[key]:
                            for childkey, childvalue in value.items():
                                app=app+f'\t{str(childvalue)}'

                else:
                    app=str(element[key])
                print(app)
                if ext in ['.xlsx', '.xls', '.csv']:
                    keystring=f'Found at Column {str(key)} : {app}'
                else:
                    keystring=f'Found at {str(key)} : {app}'
                listel='<li> '+keystring+'</li>'
                content=content+'\n'+listel
    end=f"""
      </div>
    </ul>
    </div>
    """
    content=content+'\n'+end
    return content
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
                  vallist=value.split(' ')
                  for val in vallist:
                      if str(search_term).lower() in str(val).lower() or str(search_term)==str(val):
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
              if str(search_term).lower() in str(textlist[t]).lower() or str(search_term)==str(textlist[t]):
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
    with open('search.json','w') as file:
        json.dump(search_results, file, indent=5)
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
    html_content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Search Results for """+str(search_term)+""" </title>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
        body, h1, h2, p, ul, li {
            margin: 0;
            padding: 0;
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            color: #333;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .heading {
            font-size: 30px;
            margin-bottom: 5px;
            margin-left: auto;
            margin-right: auto;
            color:#000000;
            font-family: sans-serif;
            font-weight: bold;
        }
        .writtentext {
            font-size: 16px;
            margin-bottom: 2px;
            color:#f7f7f7;
            font-family: sans-serif;
        }
        .card-container{
          display: flex;
          flex-direction: column;
          margin: 10px;
          padding: 20px;
        }
        .card{
          background-color: antiquewhite;
          margin-right: 10px;
          margin-left: 10px;
          margin-bottom: 10px;
          padding: 20px;
          border-radius: 10px;
          box-shadow: 2px 2px 2px 2px #000000;
        }

        .link-container{
          display: flex;
          flex-direction: column;
          margin: 10px;
          padding: 20px;
        }

        .list-links{
            list-style-type: square;
        }
        .link-element{
            margin: 10px 0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 2px 2px #000000;
            background-color: antiquewhite;
            font-weight: bolder;
        }
        .card-heading{
            margin: 0 auto;
        }
        .collapsible-list {
            list-style-type: none;
            margin: 0;
            padding: 0;
        }
    .collapsible-content {
    display: none;
    background-color: antiquewhite; /* Background color similar to card */
    margin: 10px;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 2px 2px 2px 2px #000000; 
    }

    .collapsible-button {
    background-color: #eee;
    color: #333;
    cursor: pointer;
    padding: 10px;
    width: 100%;
    text-align: left;
    border: none;
    outline: none; 
    }

   .collapsible-button:hover {
    background-color: #ccc;
    }

    </style>
    </head>
    <body>
        <div class="heading">
            <p class="heading">Search Results for """ + str(search_term) +""" </p>
        </div>
                    <div class="card-container">
    """
    for res in search_results:
        card_content=create_card_content(res)
        html_content=html_content+'\n'+card_content
    html_content=html_content+"""
            </div>
            <div class="link-container">
                <div class="heading">
                <p class="heading">
                    We have also searched the Web for a few good links for you
                </p>
                </div>
                <ul class="list-links">
    """
    for alink in dicoflinks:
        linkcontent=f"""
        <li class="link-element"><a href="{alink['href']}">{alink['name']}</a></li>
        """
        html_content=html_content+'\n'+linkcontent
    html_content=html_content+"""
                </ul>
            </div>
    <script>
       function toggleCollapsible(event) {
       var content = event.target.nextElementSibling;
       content.style.display === 'none' ? content.style.display = 'block' : content.style.display = 'none';
    }
</script>
    </body>
</html>
    """
    #print(html_content)
    output_file=f"{search_term}Results.html"
    with open(output_file, 'w') as f:
        f.write(html_content)
    curr_dir=os.path.dirname(__file__)
    file=os.path.join(curr_dir, output_file)
    openfile='file:///'+file
    webbrowser.open(openfile)


input_term=input('Enter Input Term: ')
search(input_term)



