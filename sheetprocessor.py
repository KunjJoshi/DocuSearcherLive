import pandas as pd
import os

def process_sheet(dataset, sheet_path):
    ext=os.path.splitext(os.path.basename(sheet_path))[-1]
    if ext=='.csv':
        df=pd.read_csv(sheet_path)
    elif ext=='.xls' or ext=='.xlsx':
        df=pd.read_excel(sheet_path)
    dfcolumns=list(df.columns)
    datas=pd.read_csv(dataset)
    paths=list(datas['Path'])
    texts=list(datas['Text'])
    pages=list(datas['PageNo'])
    frames=list(datas['FrameNo'])
    lines=list(datas['LineNo'])
    columns=list(datas['Column'])
    for column in dfcolumns:
        values=list(df[column])
        columns.append(column)
        coldict={}
        for i in range(len(values)):
            text_in_val=values[i]
            coldict[f'row_{i}']=text_in_val
        texts.append(coldict)
        paths.append(sheet_path)
        pages.append(None)
        lines.append(None)
        frames.append(None)
    data={'Path':paths, 'PageNo':pages, 'FrameNo':frames, 'LineNo':lines, 'Column':columns, 'Text':texts}
    df=pd.DataFrame(data)
    df.to_csv(dataset, index=False)
    return df.tail()
