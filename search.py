from googlelinkbringer import getGooglePages
import pandas as pd
import webbrowser
import os

def search(search_term):
    curr_dir=os.path.dirname(__file__)
    i=0
    search_results=[]
    df=pd.read_csv('Dataset.csv')
    allpaths=df['Path']
    alltexts=df['Text']
    for j in range(len(alltexts)):
        textlist=alltexts[j].split(' ')
        for t in range(len(textlist)):
            if search_term in textlist[t] or search_term==textlist[t]:
                i=i+1
                searchdict={}
                searchdict['result']=i
                searchdict['path']=allpaths[j]
                searchdict['pathhref']='file:///'+os.path.join(curr_dir, allpaths[j])
                searchdict['position']=t
                excerpt='...'
                if t>=1:
                    for x in range(t, t-2, -1):
                        excerpt=textlist[x]+' '+excerpt
                if t<=len(textlist)-1:
                    for x in range(t, t+1):
                        excerpt=excerpt+' '+textlist[x]
                excerpt=excerpt+'...'
                searchdict['excerpt']=excerpt
                search_results.append(searchdict)
    links=getGooglePages(search_term)
    dicoflinks=[]
    for link in links:
        linker=link.split('.')
        linkdict={}
        linkdict['name']=linker[0]
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
        }
        .card-heading{
            margin: 0 auto;
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
        card_content=f"""
                <div class="card">
                    <p class="card-heading"><strong> Result {res['result']}</strong></p>
                    <a href="{res['pathhref']}"class="text"><strong>Path to Result:</strong> {res['path']}</a>
                     <p class="text"><strong>Result found at Position</strong>:{res['position']}</p>
                     <p class="text"><strong>Excerpt:</strong> {res['excerpt']}</p>
                </div>
"""
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
    </body>
</html>
    """
    print(html_content)
    output_file=f"{search_term}Results.html"
    with open(output_file, 'w') as f:
        f.write(html_content)
    curr_dir=os.path.dirname(__file__)
    file=os.path.join(curr_dir, output_file)
    openfile='file:///'+file
    webbrowser.open(openfile)


input_term=input('Enter Input Term: ')
search(input_term)



