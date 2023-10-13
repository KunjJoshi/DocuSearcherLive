from googlelinkbringer import getGooglePages
import pandas as pd
def makeSearch(query, opfilename):
    df=pd.read_csv('Dataset.csv')
    alltexts=list(df['Text'])
    allpaths=list(df['Path'])
    results=[]
    try:
        for ind,text in enumerate(alltexts):
            resdict={}
            if query in text:
                resdict['Text']=text
                resdict['Query']=query
                resdict['Position']=text.find(query)
                resdict['Path']=allpaths[ind]
                results.append(resdict)
        data=f'\t\tFound Results for Query: {query}'
        for result in results:
            data=data+'Found Query in File: '+result['Path']+'\t Found Text in File: '+result['Text']+'\tFound Query at Position: '+result['Position']+'\t\n'
        googleLinks=getGooglePages(query)
        data=data+'\n\t\tFound Some More results for you from Google. FOllow the below given links: \n'
        for link in googleLinks:
            data=data+' '+link+'\n'
        with open(opfilename,'w') as file:
            file.write(data)
        return 'Search Results Found'
    except Exception as e:
        print(e)
        return 'Search Failed'

searchSuccess=makeSearch('government','governmentResults.txt')
print('Government Result: ', searchSuccess)

searchSuccess=makeSearch('food','foodResults.txt')
print('Food Result: ', searchSuccess)

